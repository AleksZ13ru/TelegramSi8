from __future__ import absolute_import, unicode_literals
import os
# import time

from celery import Celery
# from py_telegram.tasks import message_task

# set the default Django settings module for the 'celery' program.
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TelegramSi8.settings')

app = Celery('TelegramSi8')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def test(arg):
    print(arg)
