# -*- coding: utf-8 -*-
import time
from django.utils import timezone
import asyncio
from si8_parsing.TOwen import Owen3
from si8_parsing.TSystem import MySerial3
from si8_parsing.models import ComPort, Machine, Value
import threading
from .models import Date


def threading_read_in_model():
    date_now = timezone.now().date()
    # current_date = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
    Date.objects.get_or_create(date=date_now)

    comports = ComPort.objects.filter(enable=True)
    for comport in comports:
        # read_machine_in_model(comport=comport)  # use in debug
        my_thread = threading.Thread(target=read_machine_in_model, args=(comport,))
        my_thread.start()


def read_machine_in_model(comport):
    try:
        COM = MySerial3.ComPort(port=comport.port_name, baudrate=comport.baud_rate, timeout=comport.timeout)
    except Owen3.OwenPortNotOpenError:
        print('Error openning port!')
        raise Exception('Error openning port!')
    machines = Machine.objects.filter(com_port=comport, enable=True)
    for machine in machines:
        result = 0
        status = 0
        try:
            # result = Owen3.OwenDevice(COM, machine.register).GetBCD('DCNT')
            result = Owen3.OwenDevice(COM, machine.register).GetBCD('DSPD')
            status = 1
            print('%d:%s = %s' % (machine.register, machine.title, result.__str__()))
        except Owen3.OwenProtocolError:
            print('%d:%s = --.-' % (machine.register, machine.title))
        Value.add_in_com_port1(register=machine.register, meaning=result, status=status)


def read_device():
    portName = '/dev/ttyUSB0'
    baudRate = 4800
    try:
        COM = MySerial3.ComPort(portName, baudRate, timeout=0.5)
    except:
        raise Exception('Error openning port!')
    SI8_1 = Owen3.OwenDevice(COM, 17)
    SI8_2 = Owen3.OwenDevice(COM, 1)
    SI8_3 = Owen3.OwenDevice(COM, 5)
    # while True:
    try:
        result = SI8_1.GetBCD('DCNT')
        print('SI8_1 = ' + result.__str__())
    except Owen3.OwenProtocolError:
        print('SI8_1 = --.-')
    try:
        result = SI8_2.GetBCD('DCNT')
        print('SI8_2 = ' + result.__str__())
    except Owen3.OwenProtocolError:
        print('SI8_2 = --.-')
    try:
        result = SI8_3.GetBCD('DCNT')
        print('SI8_3 = ' + result.__str__())
    except Owen3.OwenProtocolError:
        print('SI8_3 = --.-')


if __name__ == '__main__':
    threading_read_in_model()
