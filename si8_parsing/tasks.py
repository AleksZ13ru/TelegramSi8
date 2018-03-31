from __future__ import absolute_import, unicode_literals

from django.utils import timezone
from celery import shared_task

from si8_parsing.models import File
from si8_parsing.code2 import find_file, open_files


'''
функция проверяет состояние оборудования, и при обнаруженнии останова - запуска машины,
формирует сообщение для заинтересованных пользователей.
'''


@shared_task(name='si8_parsing.tasks.parsing_files_task')
def parsing_files_task():
    find_file()
    files = File.objects.filter(parsing_status=0)
    print('%s найдено: %d файлов' % (timezone.now(), len(files)))
    # time.sleep(5)  # 10 sec.
    for f in files:
        print('%s : %s начат разбор' % (timezone.now(), f.name))
        open_files(f.id)
        print('%s : %s завершен разбор' % (timezone.now(), f.name))
