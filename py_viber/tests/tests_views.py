from django.conf import settings
from django.test import TestCase
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from py_viber.views import find_email, parse_valid_cmd
from py_viber.models import User


class ViberTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_viber_verify_signature(self):
        bot_configuration = BotConfiguration(name='SKableBot', avatar='http://viber.com/avatar.jpg',
                                             auth_token=settings.VIBER_BOT_TOKEN)
        viber = Api(bot_configuration)
        request_header = '28a9c7dba31408c8fab26fb494ff45cf3b429a937b5ba5dcb196c6c5384682ef'
        message = b'{"event":"message","timestamp":1523995645924,"message_token":5167121934301882005,"sender":{"id":"o6yM3j5V4I264DuHgS4MaQ==","name":"\u0410\u043B\u0435\u043A\u0441\u0430\u043D\u0434\u0440 \u0417\u0430\u0439\u043A\u0438\u043D","avatar":"https://media-direct.cdn.viber.com/download_photo?dlid=ymOEPZPXZ8abkbJHPaCYyaon2alAxqGUJE6iuEAs_csxuEGTUihoZ8wh1veyJvet9vkThmlLffOAj6dnNAbWhS5oek2GBIgV4OzdrqI-pDEl58d7ikt3JGsNHKPb08cCQ2O9pw&fltp=jpg&imsz=0000","language":"ru","country":"RU","api_version":5},"message":{"text":"1","type":"text"},"silent":false}'
        self.assertTrue(viber.verify_signature(message, request_header))


class ParseCmdTestClass(TestCase):
    commands_valid = {
        'add': '',
        'black': '',
        'pausa': ''

    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Иван', viber_id='u2NYcWleYQgJQkgYdDhfzg==', role='VALID_VERIF', email='a.a@b.b')
        User.objects.create(first_name='Петр', viber_id='u2NYcWleYQgJQkgYdDhfzg==', role='SU_VALID', email='a.a@b.b')
        pass

    def setUp(self):
        pass

    def test_parse_valid_cmd(self):
        cmd = 'add u2NYcWleYQgJQkgYdDhfzg=='
        result_test = {'cmd': 'add', 'viber_id': 'u2NYcWleYQgJQkgYdDhfzg=='}
        self.assertEqual(parse_valid_cmd(cmd, self.commands_valid), result_test)


class EmailTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_find_email_none(self):
        cmd = ''
        self.assertEqual(find_email(cmd), None)

    def test_find_email(self):
        cmd = 'Abra l.admin@admin.com kadabra'
        self.assertEqual(find_email(cmd), 'l.admin@admin.com')
