from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import File
from .code2 import findfile, parsing_si8
from django.utils import timezone

'''
функция проверяет состояние оборудования, и при обнаруженнии останова - запуска машины,
формирует сообщение для заинтересованных пользователей.
'''


# @shared_task
# def loop_task():
#     # loops = Loop.objects.all()
#     # value_changes = ValueChange.objects.all()
#     loops = Loop.objects.all()
#     for loop in loops:
#         value_change = ValueChange.objects.get(machine_id=loop.machine_id)
#         timedelta = value_change.change_datetime - loop.trigger_datetime
#         if (loop.trigger_value == 0 and value_change.change_value != 0) or (
#                 loop.trigger_value != 0 and value_change.change_value == 0):
#             if timedelta.seconds > 600:
#                 print("Z-Z-Z")
#                 loop.trigger_datetime= value_change.change_datetime
#                 loop.trigger_value = value_change.change_value
#                 loop.save()
#                 message = Message.objects.create(user=loop.user, text='Hello main frainds!')
#                 message.save()
#
#
# @shared_task
# def message_task():
#     messages = Message.objects.filter(status='READY')
#     for message in messages:
#         TelegramBot.sendMessage(message.user.telegram_id, message.text)
#         message.status = 'POST'
#         message.date_status = timezone.now()
#         message.save()


@shared_task(name='si8_parsing.tasks.parsing_files_task')
def parsing_files_task():
    findfile()
    files = File.objects.filter(parsing_status=0)
    print('%s найдено: %d файлов' % (timezone.now(), len(files)))
    # time.sleep(5)  # 10 sec.
    for f in files:
        print('%s : %s начат разбор' % (timezone.now(), f.name))
        parsing_si8(f.id)
        print('%s : %s завершен разбор' % (timezone.now(), f.name))
