# -*- coding: utf-8 -*-
import time
import asyncio
from si8_parsing.TOwen import Owen3
from si8_parsing.TSystem import MySerial3
from si8_parsing.models import ComPort, Machine, Value
import threading

def read_device_in_model():
    comports = ComPort.objects.filter(enable=True)
    for comport in comports:
        portName = comport.port_name
        baudRate = comport.baud_rate
        try:
            COM = MySerial3.ComPort(portName, baudRate, timeout=0.5)
        except:
            raise Exception('Error openning port!')
        machines = Machine.objects.filter(com_port=comport)
        for machine in machines:
            try:
                # result = Owen3.OwenDevice(COM, machine.register).GetBCD('DCNT')
                result = Owen3.OwenDevice(COM, machine.register).GetBCD('DSPD')
                Value.add_in_com_port(register=machine.register, meaning=result)
                print('%d:%s = %s' % (machine.register, machine.title, result.__str__()))
            except Owen3.OwenProtocolError:
                Value.add_in_com_port(register=machine.register, meaning=0)
                print('%d:%s = --.-' % (machine.register, machine.title))


def coms_read_in_model():
    comports = ComPort.objects.filter(enable=True)
    reads = [asunc_read_machine_in_model(comport) for comport in comports]
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(reads))
    loop.run_until_complete(asyncio.wait(reads))


def threading_read_in_model():
    comports = ComPort.objects.filter(enable=True)
    for comport in comports:
        my_thread = threading.Thread(target=read_machine_in_model, args=(comport,))
        my_thread.start()


def read_machine_in_model(comport):
    portName = comport.port_name
    baudRate = comport.baud_rate
    try:
        COM = MySerial3.ComPort(portName, baudRate, timeout=0.5)
    except:
        raise Exception('Error openning port!')
    machines = Machine.objects.filter(com_port=comport)
    for machine in machines:
        try:
            # result = Owen3.OwenDevice(COM, machine.register).GetBCD('DCNT')
            result = Owen3.OwenDevice(COM, machine.register).GetBCD('DSPD')
            Value.add_in_com_port1(register=machine.register, meaning=result, status=1)
            print('%d:%s = %s' % (machine.register, machine.title, result.__str__()))
        except Owen3.OwenProtocolError:
            Value.add_in_com_port1(register=machine.register, meaning=0, status=0)
            print('%d:%s = --.-' % (machine.register, machine.title))


@asyncio.coroutine
def asunc_read_machine_in_model(comport):
    portName = comport.port_name
    baudRate = comport.baud_rate
    try:
        COM = MySerial3.ComPort(portName, baudRate, timeout=0.5)
    except:
        raise Exception('Error openning port!')
    machines = Machine.objects.filter(com_port=comport)
    for machine in machines:
        try:
            # result = Owen3.OwenDevice(COM, machine.register).GetBCD('DCNT')
            result = Owen3.OwenDevice(COM, machine.register).GetBCD('DSPD')
            Value.add_in_com_port1(register=machine.register, meaning=result, status=1)
            print('%d:%s = %s' % (machine.register, machine.title, result.__str__()))
        except Owen3.OwenProtocolError:
            Value.add_in_com_port1(register=machine.register, meaning=0, status=0)
            print('%d:%s = --.-' % (machine.register, machine.title))
    # time.sleep(5)


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
    # read_device_in_model()
    # coms_read_in_model()
    threading_read_in_model()



