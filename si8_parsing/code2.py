from __future__ import absolute_import
import time
import os
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Folder, File, Value, Machine
from .code.parsing import parsing_file


# вызывать 1  раз в минуту
# ищет в папке файлы с расширением si8,
# если файла с таким хешем нет, то добавляет в базу - модель File
# @shared_task
def find_file():
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
    try:
        with open(path + filename, 'rb') as f:
            m = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return_hash = m.hexdigest()
    except FileNotFoundError:
        return_hash = None
    return return_hash


# {'value': 51.8, 'now_date': datetime.datetime(2016, 12, 26, 7, 30), 'id_si8': 1}
def open_files(pk=None):
    if pk is None:
        files = File.objects.filter(parsing_status=0)
    else:
        files = File.objects.filter(id=pk)
    for file in files:
        try:
            file.parsing_status = 2
            file.save()
            ds = parsing_file(file.path, file.name)
            for d in ds['bufs']:
                try:
                    Machine.objects.get(register=d['id_si8'])
                    Value.add(register=d['id_si8'], date_now=d['now_date'], meaning=d['value'], time_stamp=3,
                              end_date=ds['end_date'])
                except ObjectDoesNotExist:
                    pass
            file.parsing_status = 1
            file.save()
        except BaseException as error:
            print('An exception occurred in parsing_si8: {}'.format(error))


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


def main():
    while True:
        find_file()
        files = File.objects.filter(parsing_status=0)
        print('%s найдено: %d файлов' % (timezone.now(), len(files)))
        # time.sleep(5)  # 10 sec.
        for f in files:
            print('%s : %s начат разбор' % (timezone.now(), f.name))
            open_files(f.id)
            print('%s : %s завершен разбор' % (timezone.now(), f.name))
        print('Пауза 300 сек.')
        time.sleep(300)  # 10 sec.


if __name__ == '__main__':
    main()
