from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Loop, Message
from si8_parsing.models import ValueChange

import telepot
from django.conf import settings

from django.utils import timezone
import time
from random import randint

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

# @shared_task
# def add(x, y):
#     return x + y
#
#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
#
#
# @shared_task
# def period():
#     print('period!')


'''
функция проверяет состояние оборудования, и при обнаруженнии останова - запуска машины,
формирует сообщение для заинтересованных пользователей.
'''


@shared_task
def loop_task0():
    # loops = Loop.objects.all()
    # value_changes = ValueChange.objects.all()
    loops = Loop.objects.all()
    for loop in loops:
        value_change = ValueChange.objects.get(machine_id=loop.machine_id)
        timedelta = value_change.change_datetime - loop.trigger_datetime
        if (loop.trigger_value != 0 and value_change.read_value == 0) or \
                (loop.trigger_value == 0 and value_change.read_value != 0):
            if timedelta.seconds > 600:
                print("Z-Z-Z")
                loop.trigger_datetime = value_change.read_datetime
                loop.trigger_value = value_change.read_value
                loop.save()
                text = '{0} : {1} = {2}'.format(value_change.machine.title, loop.trigger_datetime, loop.trigger_value)
                message = Message.objects.create(user=loop.user, text=text)
                message.save()

        # if loop.trigger_value == 0 and value_change.read_value != 0:
        #     if timedelta.seconds > 600:
        #         print("Z-Z-Z")
        #         loop.trigger_datetime = value_change.read_datetime
        #         loop.trigger_value = value_change.change_value
        #         loop.save()
        #         message = Message.objects.create(user=loop.user, text='Hello main frainds!')
        #         message.save()


@shared_task(name='py_telegram.tasks.loop_task')
def loop_task():
    # loops = Loop.objects.all()
    # value_changes = ValueChange.objects.all()
    loops = Loop.objects.all()
    for loop in loops:
        value_change = ValueChange.objects.get(machine_id=loop.machine_id)
        # timedelta = value_change.change_datetime - loop.trigger_datetime
        if loop.trigger_value != 0:
            trigger = True
        else:
            trigger = False

        if value_change.read_value != 0:
            read = True
        else:
            read = False

        if trigger != read:
            loop.trigger_hysteresis += 1
        else:
            loop.trigger_hysteresis = 0
        loop.save()

        if loop.trigger_hysteresis > 5:
            print("Z-Z-Z")
            loop.trigger_datetime = value_change.read_datetime
            loop.trigger_value = value_change.read_value
            loop.trigger_hysteresis = 0
            loop.save()
            # text = '{0} : {1} = {2}'.format(value_change.machine.title, loop.trigger_datetime, loop.trigger_value)
            text = 'Оборудование: /{0}\n'.format(value_change.machine.title)
            time_minus_five = loop.trigger_datetime.replace(minute=loop.trigger_datetime.minute - 5)
            if loop.trigger_value == 0:
                text += 'Событие: останов в {0}'.format(time_minus_five.time())
            else:
                text += 'Событие: запуск в {0}'.format(time_minus_five.time())
            message = Message.objects.create(user=loop.user, text=text)
            message.save()


@shared_task(name='py_telegram.tasks.message_task')
def message_task():
    messages = Message.objects.filter(status='READY')
    for message in messages:
        TelegramBot.sendMessage(message.user.telegram_id, message.text)
        message.status = 'POST'
        message.date_status = timezone.now()
        message.save()
