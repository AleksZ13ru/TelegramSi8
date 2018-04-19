from __future__ import absolute_import, unicode_literals
from celery import shared_task
from viberbot import BotConfiguration, Api
from viberbot.api.messages import TextMessage

from py_viber.models import Message

from django.conf import settings

from django.utils import timezone

bot_configuration = BotConfiguration(name='SKableBot',
                                     avatar='http://viber.com/avatar.jpg',
                                     auth_token=settings.VIBER_BOT_TOKEN)
viber = Api(bot_configuration)


@shared_task(name='py_viber.tasks.message_viber_task')
def message_task():
    messages = Message.objects.filter(status='READY')
    for message in messages:
        viber.send_messages(to=message.user.viber_id, messages=[TextMessage(text=message.text)])
        message.status = 'POST'
        message.date_status = timezone.now()
        message.save()
