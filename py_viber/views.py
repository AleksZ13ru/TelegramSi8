import json
import sched
import threading
import time

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from requests import Response
from requests.exceptions import ConnectionError
from datetime import datetime

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import KeyboardMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

from py_viber.models import User, Message
from si8_parsing.models import Machine, Value, ValueChange, Date
from si8_parsing.code.pack import repack

bot_configuration = BotConfiguration(name='SKableBot',
                                     avatar='http://viber.com/avatar.jpg',
                                     auth_token=settings.VIBER_BOT_TOKEN)
viber = Api(bot_configuration)


def display_obr_list(telegram_id, cmd):
    machines = Machine.objects.all().order_by('title')
    result = 'Список оборудования:\n\n'
    for m in machines:
        result += '/{0}\n\n'.format(m.title)
        pass
        # result += '{0}'.format(m.lower)
    result += '\n Вы можете указать дату в формате: Troester 13-03-18.\n'
    return result


def display_obr(telegram_id, cmd):
    result = ''
    lower = cmd['name']
    date = cmd['date']
    try:
        machine = Machine.objects.get(lower=lower)
    except ObjectDoesNotExist:
        return 'Не найдено оорудование с указанным именем!'
    try:
        # machine = Machine.objects.get(lower=lower)
        obj_data = Date.objects.get(date=date)
        value = Value.objects.get(register=machine.register, date=obj_data.id)
        string_value = repack(machine.title, value.date.date, value.value)
        for s in string_value:
            result += s
        value_change = ValueChange.objects.get(machine=machine)
        # result += '\nДанные на {0}'.format(value_change.read_datetime.time().strftime('%H:%M'))
    except ObjectDoesNotExist:
        result = 'Нет данных для /{0} на дату {1}!'.format(machine.title, date)
    return result


def ngrock_https():
    url = None
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        request_dict = json.loads(response.content.decode('utf-8'))
        tunnels = request_dict['tunnels']
        for tunnel in tunnels:
            if tunnel['proto'] == "https":
                url = tunnel['public_url']
    except ConnectionError:
        print('ConnectionError')
    return url


def set_webhook(viber):
    url = ngrock_https() + '/viber/bot/'
    if url is not None:
        viber.set_webhook(url)
    else:
        viber.set_webhook(settings.VIBER_BOT_WEBHOOK)


# scheduler = sched.scheduler(time.time, time.sleep)
# scheduler.enter(5, 1, set_webhook, (viber,))
# t = threading.Thread(target=scheduler.run)
# t.start()


def request_headers(request):
    headers = {}
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers[header] = value

    return headers


def find_email(cmd):
    result = None
    words = cmd.lower().lstrip('/').split()
    for word in words:
        if word.find('@') != -1:
            result = word
    return result


def parse_user_cmd(cmd, cmd_dict):
    result = {'cmd': None, 'name': None, 'date': None, 'param': None}  # date, name, cmd, param
    words = cmd.lower().lstrip('/').split()
    result['param'] = words.copy()
    # for word in words:
    for word in words:
        try:
            result['date'] = datetime.strptime(word, '%d-%m-%y').date()
            result['param'].remove(word)
            continue
        except ValueError:
            pass
        try:
            result['name'] = Machine.objects.get(lower=word).lower
            result['param'].remove(word)
            continue
        except ObjectDoesNotExist:
            pass
        try:
            keys = cmd_dict.keys()
            for key in keys:
                if word == key:
                    result['cmd'] = key
                    result['param'].remove(key)
                    continue
            # else: result['cmd'] = 'none'
        except KeyError:
            pass
    if result['cmd'] is None and result['name'] is not None:
        result['cmd'] = 'obr'
    if result['date'] is None:
        result['date'] = datetime.now().date()
    return result


def valid(cmd):
    text = ''
    key = {'Type': 'keyboard', 'Buttons': []}
    try:
        user = None
        if cmd['viber_id'] is not None:
            user = User.objects.get(viber_id=cmd['viber_id'], role='VALID_VERIF')
    except ObjectDoesNotExist:
        user = None
    if user is not None:
        if cmd['cmd'] == 'add':
            user.role = 'VALID_GOOD'
            user.save()
            key = {'Type': 'keyboard', 'Buttons': []}
            text = 'Пользователю {0} разрешен доступ'.format(user.first_name)
        elif cmd['cmd'] == 'black':
            user.role = 'BLACK'
            user.save()
            key = {'Type': 'keyboard', 'Buttons': []}
            text = 'Пользователь {0} занесен в черный список!'.format(user.first_name)

    if cmd['cmd'] == 'pausa':
        key = {'Type': 'keyboard', 'Buttons': [{'ActionBody': 'valid_list', 'Text': 'Список заявок'}]}
        text = 'Не забудьте проверить список заявок!'
    elif cmd['cmd'] == 'list_valid':
        key = {'Type': 'keyboard', 'Buttons': []}
        text = 'Список пользователей для подтверждения!'
    return {'text': text, 'key': key}


def parse_valid_cmd(cmd, cmd_dict):
    result = {'cmd': None, 'viber_id': None}
    words = cmd.lstrip('/').split()
    for word in words:
        keys = cmd_dict.keys()
        try:
            for key in keys:
                if word == key:
                    result['cmd'] = key
                    continue
        except KeyError:
            pass
        try:
            user = User.objects.get(viber_id=word, role='VALID_VERIF')
            result['viber_id'] = user.viber_id
        except ObjectDoesNotExist:
            pass
    return result


class CommandReceiveView(View):
    def post(self, request):
        if not viber.verify_signature(request.body, request_headers(request).get('X-Viber-Content-Signature')):
            return JsonResponse({}, status=403)

        commands_user = {
            # 'start': display_help,
            # 'help': display_help,
            # 'feed': display_planetpy_feed,
            'list': display_obr_list,
            'obr': display_obr,
            # 'loop': display_loop,
        }

        commands_valid = {
            'add': valid,
            'black': valid,
            'pausa': valid

        }

        # this library supplies a simple way to receive a request object
        viber_request = viber.parse_request(request.body.decode('utf-8'))

        if isinstance(viber_request, ViberMessageRequest):
            user_viber_id = viber_request.sender.id
            user_first_name = viber_request.sender.name
            users = User.objects.get_or_create(viber_id=user_viber_id, first_name=user_first_name)
            user = users[0]
            if user.role == 'SU_VALID':
                cmd = parse_valid_cmd(viber_request.message.text, commands_valid)
                func = commands_valid.get(cmd['cmd'])
                if func:
                    mess = func(cmd)
                    viber.send_messages(to=viber_request.sender.id,
                                        messages=[TextMessage(text=mess['text'])])
                # else:
                #     viber.send_messages(to=viber_request.sender.id,
                #                         messages=[TextMessage(text="Не удалось распознать запрос.")])

            elif user.role == 'NEW_USER':
                if user.email == '':
                    email = find_email(viber_request.message.text)
                    if email is None:
                        text = "Для получения данных из данного чата, необходима авторизация.\n " \
                               "Пожалуйста отправьте сообщение с указанием рабочей почты для Вашей регистрации."

                        # key = json.dumps(key)
                        # message = KeyboardMessage(keyboard=key)
                        # viber.send_messages(to=viber_request.sender.id, messages=message)
                    else:
                        user.email = email
                        user.role = 'VALID'
                        user.save()
                        # su_valids = User.objects.filter(role='SU_VALID')
                        # for su in su_valids:
                        #     Message.objects.create(user=su,
                        #                            text='Новый пользователь! {0} : {1}\n Добавить клавиатуру действий'
                        #                            .format(user.first_name, user.email))
                        text = "От Вас получен адрес электонной почты\n " \
                               "После подтверждения администратором, Вы сможете получать информацию из данного чата."
                else:
                    text = "Ваша учетная запись находится на проверке!"
                # key = {'Type': 'keyboard', 'Buttons': [
                #     {'ActionType': 'reply', 'ActionBody': 'add', 'Text': 'Добавить пользователя'},
                #     {'ActionType': 'reply', 'ActionBody': 'black', 'Text': 'В черный список'},
                #     {'ActionType': 'reply', 'ActionBody': 'pausa', 'Text': 'Отложить решение'},
                #
                # ]}
                # keymess = KeyboardMessage(keyboard=key)
                # mess = [TextMessage(text=text), keymess]
                viber.send_messages(to=viber_request.sender.id, messages=[TextMessage(text=text)])
            if user.role == 'USER' or user.role == 'SU_USER' or user.role == 'SU_VALID':
                # message = viber_request.message
                cmd = parse_user_cmd(viber_request.message.text, commands_user)
                func = commands_user.get(cmd['cmd'])
                if func:
                    # message = viber_request.message
                    # lets echo back
                    text = func(user_viber_id, cmd)
                    viber.send_messages(viber_request.sender.id, messages=[TextMessage(text=text)])
                else:
                    viber.send_messages(to=viber_request.sender.id,
                                        messages=[TextMessage(text="Не удалось распознать запрос.")])
            elif user.role == 'BLACK':
                viber.send_messages(to=viber_request.sender.id,
                                    messages=[TextMessage(text="Ваша профиль не авторизован!")])
            # else:
            #     viber.send_messages(to=viber_request.sender.id,
            #                         messages=[TextMessage(text="Не удалось распознать запрос.")])
        elif isinstance(viber_request, ViberSubscribedRequest):
            viber.send_messages(viber_request.user.id, [
                TextMessage(text="thanks for subscribing!")
            ])
        elif isinstance(viber_request, ViberFailedRequest):
            pass
            # logger.warn("client failed receiving message. failure: {0}".format(viber_request))

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
