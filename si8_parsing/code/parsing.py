# from datetime import datetime
from django.utils import timezone
import random
import struct
# import datetime
import os
import logging


def openfilesi8(foldeder, filename):
    logtime = timezone.now()
    # foldeder = 'data/'
    # filename = '010913.SI8'
    with open(foldeder + filename, "rb") as f:
        count_line = 0
        count_si8 = 1
        bufs = []
        while count_si8:
            count_si8 = int.from_bytes(f.read(1), byteorder='big')
            hour = int.from_bytes(f.read(1), byteorder='big')
            minute = int.from_bytes(f.read(1), byteorder='big')
            if minute >= 60:
                minute = 59
            # print("Счетчиков = %d, Время %d:%d" % (count_si8, hour, minute))
            for i in range(1, count_si8 + 1, 1):
                # addr = f.read(1)
                addr = int.from_bytes(f.read(1), byteorder='big')
                data = f.read(4)
                speed = struct.unpack('f', data)[0]
                # print("Счетчик = %d, Скорость=%.2f" % (addr, speed))
                d1 = timezone.datetime.strptime(filename[0:6], '%d%m%y')
                dstart = d1.replace(hour=7, minute=30)
                date = d1.replace(hour=hour, minute=minute)
                if date < dstart:
                    delta = timezone.timedelta(days=1)  # дельта в 1 дня
                    date = date + delta
                if addr != 0:
                    try:
                        # print("Дата = %s, Счетчик = %d, Скорость=%.2f" % (date, addr, speed))
                        count_line += 1
                        # 30-01-1987 13:12
                        datestr = date.strftime('%d-%m-%Y %H:M')
                        buf = {'id_si8': addr, 'value': round(speed, 2), 'now_date': date, 'datestr': datestr}
                        bufs.append(buf)

                        # time.sleep(1)
                    except Exception:
                        pass
                        # print("Error - Дата = %s, Счетчик = %d, Скорость=%.2f" % (date, addr, speed))
                        # print("error")
    # print("Всего полей =  %s" % count_line)
    ss = ('%s - %s' % (logtime.second, timezone.now().second))
    return bufs
    # return {'bufs': bufs, 'counter': count_line}


# для разбора файлов si8, есть не доработана
def openfilesi8_v2(foldeder, filename):
    logtime = timezone.now()
    # foldeder = 'data/'
    # filename = '010913.SI8'
    with open(foldeder + filename, "rb") as f:
        count_line = 0
        count_si8 = 1
        bufs = []
        end_date = None
        result ={}
        while count_si8:
            count_si8 = int.from_bytes(f.read(1), byteorder='big')
            hour = int.from_bytes(f.read(1), byteorder='big')
            minute = int.from_bytes(f.read(1), byteorder='big')
            if minute >= 60:
                minute = 59
            # print("Счетчиков = %d, Время %d:%d" % (count_si8, hour, minute))
            for i in range(1, count_si8 + 1, 1):
                # addr = f.read(1)
                addr = int.from_bytes(f.read(1), byteorder='big')
                data = f.read(4)
                speed = struct.unpack('f', data)[0]
                # print("Счетчик = %d, Скорость=%.2f" % (addr, speed))
                d1 = timezone.datetime.strptime(filename[0:6], '%d%m%y')
                dstart = d1.replace(hour=7, minute=30)
                date = d1.replace(hour=hour, minute=minute)
                if date < dstart:
                    delta = timezone.timedelta(days=1)  # дельта в 1 дня
                    date = date + delta
                if addr != 0:
                    try:
                        b_replica = False
                        for b in bufs:
                            if addr == b['id_si8'] and date.date() == b['now_date'].date():
                                b_replica = True
                                lvalue = b['value']
                                current_time = date.time()
                                total_minute = (current_time.hour * 60 + current_time.minute)
                                if len(lvalue) < total_minute - 1:
                                    for ii in range(total_minute - len(lvalue)):
                                        lvalue.append(0)
                                lvalue.append(round(speed, 2))
                                b['value'] = lvalue
                        if b_replica is not True:
                            buf = {'id_si8': addr, 'now_date': date, 'value': []}
                            current_time = date.time()
                            total_minute = (current_time.hour * 60 + current_time.minute)
                            lvalue = buf['value']
                            if len(lvalue) < total_minute - 1:
                                for ii in range(total_minute - len(lvalue)):
                                    lvalue.append(0)
                            lvalue.append(round(speed, 2))
                            buf['value'] = lvalue
                            bufs.append(buf)
                    except Exception:
                        pass
                if (end_date is None) or (date > end_date):
                    end_date = date
    result['bufs'] = bufs
    result['end_date'] = end_date
    return result
