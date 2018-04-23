from django.conf import settings
from django.test import TestCase
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from py_viber.views import find_email, key_valid_create, parse_valid_cmd
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
        request_header = '95a958f90bb88a0ef5312c2511e1c56650b968a37eb75f1e7326ebf52c1c9667'
        message = b'{"event":"message","timestamp":1524508607514,"message_token":5169273451608157073,"sender":{"id":"u2NYcWleYQgJQkgYdDhfzg==","name":"\\u0410\\u043B\\u0435\\u043A\\u0441\\u0430\\u043D\\u0434\\u0440 \\u0417\\u0430\\u0439\\u043A\\u0438\\u043D","avatar":"https://media-direct.cdn.viber.com/download_photo?dlid=PSF1BfvQJ9A1-blH6-shscNy-C3JnI4ax6BfvHWwdLyEAVEN_Obs-JD0DrUo6yVL_Y4Mokd8iyLhBA9a-KMVC7mXjWOEe5xDUy9htktinG1c9_lY5ejsWI8O3_T2sfjipqCj4g&fltp=jpg&imsz=0000","language":"ru","country":"RU","api_version":5},"message":{"text":"hello","type":"text"},"silent":false}'
        self.assertTrue(viber.verify_signature(message, request_header))


class KeyValidCreateTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_key_valid_create(self):
        result_test = {
            'Buttons': [{'ActionBody': 'add VG0XaHADaH/+Yn6Aan0PbA==', 'Text': 'Добавить пользователя AleksZ2'},
                        {'ActionBody': 'black VG0XaHADaH/+Yn6Aan0PbA==', 'Text': 'В черный список AleksZ2'},
                        {'ActionBody': 'pausa VG0XaHADaH/+Yn6Aan0PbA==', 'Text': 'Отложить решение AleksZ2'}],
            'Type': 'keyboard'}
        self.assertEqual(key_valid_create(user_id='VG0XaHADaH/+Yn6Aan0PbA==', name='AleksZ2'), result_test)


class ParseCmdTestClass(TestCase):
    commands_valid = {
        'add': '',
        'black': '',
        'pausa': ''

    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Иван', viber_id='u2NYcWleYQgJQkgYdDhfzg==', role='NEW_USER', email='a.a@b.b')
        # User.objects.create(first_name='Петр', viber_id='u2NYcWleYQgJQkgYdDhfzg==', role='SU_VALID', email='a.a@b.b')
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
