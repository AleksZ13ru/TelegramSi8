# from django.db import transaction
from __future__ import absolute_import

from datetime import datetime
import time
from django.utils import timezone

from .models import Folder, File, Value, Machine
import os
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from .code.parsing import openfilesi8_v2


# вызывать 1  раз в минуту
# ищет в папке файлы с расширением si8,
# если файла с таким хешем нет, то добавляет в базу - модель File
# @shared_task
def findfile():
    folders = Folder.objects.filter(enable=True)
    for folder in folders:
        trees = os.walk(folder.path)
        for tree in trees:
            for file in tree[2]:
                if file.endswith('.SI8') is True:
                    name = file
                    path = tree[0] + '/'
                    hash = get_hash_md5(path, name)
                    try:
                        f = File.objects.get(name=name)
                        if f.hash != hash:
                            print("File is modify!")
                            f.parsing_status = 0
                            f.hash = hash
                            f.save()
                    except ObjectDoesNotExist:
                        print("Add File in DB")
                        f = File(name=name, path=path, parsing_status=0, hash=hash)
                        f.save()


def get_hash_md5(path, filename):
    with open(path + filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


# {'value': 51.8, 'now_date': datetime.datetime(2016, 12, 26, 7, 30), 'id_si8': 1}
def parsing_si8(pk=None):
    if pk is None:
        files = File.objects.filter(parsing_status=0)
    else:
        files = File.objects.filter(id=pk)
    for file in files:
        try:
            file.parsing_status = 2
            file.save()
            # ds = openfilesi8(file.path, file.name)
            ds = openfilesi8_v2(file.path, file.name)
            for d in ds['bufs']:
                try:
                    Machine.objects.get(register=d['id_si8'])
                    Value.add(register=d['id_si8'], date_now=d['now_date'], meaning=d['value'], time_stamp=3,
                              end_date=ds['end_date'])
                except ObjectDoesNotExist:
                    pass
            file.parsing_status = 1
            file.save()

            # for d in ds:
            #     logtime =timezone.now()
            #     register_addr = d['id_si8']
            #     now_date = d['now_date']  # .strftime('%m/%d/%Y %H:%M')
            #     value = d['value']
            #     # reg = Register.objects.get(register_addr=register_addr)
            #     # p = PollResult(pollresult_register=reg, pollresult_time=now_date, pollresult_value=value)
            #     # p.save()
            #     ss = ('%s - %s' % (logtime.second, timezone.now().second))
            #     pass
            #     Value2.add(register=register_addr, date_now=now_date, meaning=value, time_stamp=3)
            # file.parsing_status = 1
            # file.save()
        except BaseException as error:
            print('An exception occurred in parsing_si8: {}'.format(error))


# result = [{'start': 1, 'value': [1.85, 33.3, 5.55]},
#           {'start': 6, 'value': [3.7]},
#           {'start': 9, 'value': [11.1, 59.2, 79.55, 81.4]}
#           ]

def repack_time_line():
    trend = [0, 1.85, 33.3, 5.55, 0, 0, 3.7, 0, 0, 11.1, 59.2, 79.55, 81.4]
    start_time = -1
    stop_time = -1
    value = []
    values = []

    for i in trend:
        if trend[i] is not 0:
            start_time = i
        elif trend[i] is 0 and start_time is not -1:
            stop_time = i
        if start_time is not -1 and stop_time is not -1:
            start = start_time
            for j in range(stop_time - start_time):
                value.append(trend[j])
            element = {'start': start, 'value': value}
            values.append(element)
            start_time = -1
            stop_time = -1
            value = []
    pass
    # return values


def terminal_run():
    while True:
        findfile()
        files = File.objects.filter(parsing_status=0)
        print('%s найдено: %d файлов' % (timezone.now(), len(files)))
        # time.sleep(5)  # 10 sec.
        for f in files:
            print('%s : %s начат разбор' % (timezone.now(), f.name))
            parsing_si8(f.id)
            print('%s : %s завершен разбор' % (timezone.now(), f.name))
        print('Пауза 300 сек.')
        time.sleep(300)  # 10 sec.
