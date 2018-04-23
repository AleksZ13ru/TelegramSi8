from __future__ import absolute_import, unicode_literals
from celery import shared_task
from viberbot import BotConfiguration, Api
from viberbot.api.messages import TextMessage, KeyboardMessage

from py_viber.models import User, Message

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
        if message.key is not None:
            viber.send_messages(to=message.user.viber_id, messages=[TextMessage(text=message.text, keyboard=message.key)])
        else:
            viber.send_messages(to=message.user.viber_id, messages=[TextMessage(text=message.text)])
        message.status = 'POST'
        message.date_status = timezone.now()
        message.save()


ROLE_STAT = (
    ('USER', 'User'),
    ('SU_USER', 'Superuser'),
    ('NEW_USER', 'New user'),
    ('VALID', 'Valid user'),  # пользователь ввел адрес почты, ожидает проверки
    ('VALID_VERIF', 'Valid user verif'),  # пользователь ожидает решение проверки
    ('VALID_GOOD', 'Valid good'),  # проверка пройдена, ожидается отправка сообщения о завершении проверки
    ('SU_VALID', 'Super valid user'),  # администратор, для принятия новых пользователей
    ('ADMIN', 'Admin'),
    ('BLACK', 'Blacklist user')  # черный список пользователей
)


@shared_task(name='py_viber.tasks.message_viber_create')
def message_create():
    users_valid = User.objects.filter(role='VALID')
    users_su_valid = User.objects.filter(role='SU_VALID')[0]
    for user in users_valid:
        text = 'Пользователь:{0} указал почту: {1} при регистрации! \
        Добавить его в чат?'.format(user.first_name, user.email)
        commands = {'add': 'Добавить пользователя',
                    'black': 'В черный список',
                    'pausa': 'Отложить решение'}
        buttons = []
        for command in commands:
            button = {'ActionBody': '{0} {1}'.format(command, user.viber_id),
                      'Text': '{0} {1}'.format(commands[command], user.first_name)}
            buttons.append(button)

        key = {'Type': 'keyboard', 'Buttons': buttons}
        viber.send_messages(to=users_su_valid.viber_id, messages=[TextMessage(text=text, keyboard=key)])
        user.role = 'VALID_VERIF'
        user.save()
        # viber.send_messages(to=users_su_valid.viber_id, messages=[KeyboardMessage(keyboard=key)])

    users_valid = User.objects.filter(role='VALID_GOOD')
    for user in users_valid:
        text = 'Ваша заявка одобрена!'
        Message.objects.create(user=user, text=text, status='READY')
        user.role = 'USER'
        user.save()
