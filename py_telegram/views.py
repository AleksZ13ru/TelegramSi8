# -*- coding: utf8 -*-

import json
import logging

import telepot
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import parse_planetpy_rss

from si8_parsing.models import Machine, Value, Date
from si8_parsing.code.pack import repack
from .models import User, Loop
from datetime import datetime

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


def django(request):
    return render(request, 'django.html')


def display_help(*args):
    return render_to_string('help.md')


def display_planetpy_feed(*args):
    return render_to_string('feed.md', {'items': parse_planetpy_rss()})


def display_obr_list(telegram_id, cmd):
    machines = Machine.objects.all()
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
        # machine = Machine.objects.get(lower=lower)
        obj_data = Date.objects.get(date=date)
        value = Value.objects.get(register=machine.register, date=obj_data.id)
        string_value = repack(machine.title, value.date, value.value)
        for s in string_value:
            result += s
    except ObjectDoesNotExist:
        result = 'Нет данных для %s на дату %s' % (lower, date)
    return result


def display_loop(telegram_id, cmd):
    result = ''
    machine_name_lower = cmd['name']
    # date = cmd['date']
    user = User.objects.get(telegram_id=telegram_id)
    # machine = Machine.objects()
    # machine = Machine.objects

    if machine_name_lower is None:
        try:
            loops = Loop.objects.filter(user=user)
            if len(loops) > 0:
                result = 'Список отслеживаемого Вами оборудования:\n\n'
                for loop in loops:
                    result += '/%s\n\n' % loop.machine
            else:
                result = 'У Вас еще не выбрано оборудования для отслеживания!'
            # result += '\n Для удаления : loop_del Name\n '
            # result += '\n Для добавления : loop_add Name\n '

        except ObjectDoesNotExist:
            result = 'У Вас еще не выбрано оборудования для отслеживания!'
    else:
        try:
            machine = Machine.objects.get(lower=machine_name_lower)
        except ObjectDoesNotExist:
            return 'Не найдено оорудование с указанным именем!'
        try:
            loop = Loop.objects.get(user=user, machine=machine)
            loop.delete()
            result += 'Из Вашего списка отслеживания удалено:\n /%s\n' % machine_name_lower
        except ObjectDoesNotExist:
            loop = Loop.objects.create(user=user, machine=machine)
            loop.save()
            result = 'В Ваш список отслеживания добавлено:\n /%s\n' % machine_name_lower
    return result


def parse_cmd(cmd, cmd_dict):
    result = {'cmd': None, 'name': None, 'date': None, 'param': None}  # date, name, cmd, param
    words = cmd.lower().lstrip('/').split()
    result['param'] = words.copy()
    # for word in words:
    for word in words:
        try:
            result['date'] = datetime.strptime(word, '%d-%m-%y')
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


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            'start': display_help,
            'help': display_help,
            'feed': display_planetpy_feed,
            'list': display_obr_list,
            'obr': display_obr,
            'loop': display_loop,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            user_telegram_id = payload['message']['from']['id']
            user_first_name = payload['message']['from']['first_name']
            user = User.objects.get_or_create(telegram_id=user_telegram_id, first_name=user_first_name)
            chat_id = payload['message']['chat']['id']
            if user[0].role == 'USER' or user[0].role == 'SU_USER':
                cmd = parse_cmd(payload['message'].get('text'), commands)
                func = commands.get(cmd['cmd'])
                if func:
                    TelegramBot.sendMessage(chat_id, func(user_telegram_id, cmd), parse_mode='Markdown')
                else:
                    TelegramBot.sendMessage(chat_id, 'Не удалось распознать запрос.')
            elif user[0].role == 'BLACK':
                TelegramBot.sendMessage(chat_id, 'Ваша профиль занесен в черный список!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
