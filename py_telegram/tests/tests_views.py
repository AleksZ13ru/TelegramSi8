from django.test import TestCase
from py_telegram.views import parse_cmd, display_loop
# from py_telegram.views import display_help, display_planetpy_feed, display_obr_list, display_obr
from datetime import datetime
from si8_parsing.models import Machine
from py_telegram.models import User, Loop


class ParseCmdTestClass(TestCase):
    commands = {'start': None, 'help': None, 'feed': None, 'list': None, 'obr': None, 'none': None}

    @classmethod
    def setUpTestData(cls):
        pass
        # Set up non-modified objects used by all test methods
        Machine.objects.create(title='Troester', lower='troester', register=123)

    def setUp(self):
        pass

    def test_parse_cmd_cmd_name_date(self):
        cmd = 'obr Troester 12-03-18'
        result_test = {'cmd': 'obr', 'name': 'troester', 'date': datetime(2018, 3, 12, 0, 0), 'param': []}
        self.assertEqual(parse_cmd(cmd, self.commands), result_test)

    def test_parse_cmd_name_date(self):
        cmd = 'Troester 12-03-18'
        result_test = {'cmd': 'obr', 'name': 'troester', 'date': datetime(2018, 3, 12, 0, 0), 'param': []}
        self.assertEqual(parse_cmd(cmd, self.commands), result_test)

    def test_parse_cmd_tire(self):
        cmd = 'Troester_1 12-03-18'
        result_test = {'cmd': None, 'name': None, 'date': datetime(2018, 3, 12, 0, 0), 'param': ['troester_1']}
        self.assertEqual(parse_cmd(cmd, self.commands), result_test)

    def test_parse_cmd_date_param(self):
        cmd = '12-03-18 1Troester start'
        result_test = {'cmd': 'start', 'name': None, 'date': datetime(2018, 3, 12, 0, 0), 'param': ['1troester']}
        self.assertEqual(parse_cmd(cmd, self.commands), result_test)

    def test_parse_cmd_name(self):
        cmd = 'Troester'
        result_test = {'cmd': 'obr', 'name': 'troester', 'date': datetime.now().date(), 'param': []}
        self.assertEqual(parse_cmd(cmd, self.commands), result_test)


class DisplayLoopTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass
        # Set up non-modified objects used by all test methods
        Machine.objects.create(title='Troester', lower='troester', register=123)
        User.objects.create(first_name='Anton', telegram_id=123456789)
        # Loop.objects.create(machine=machine, user=user)

    def test_add(self):
        telegram_id = 123456789
        cmd = {'cmd': 'loop', 'name': 'troester', 'date': None, 'param': None}  # date, name, cmd, param
        result_test = 'В Ваш список отслеживания добавлено:\n /troester\n'
        self.assertEqual(display_loop(telegram_id, cmd), result_test)

    def test_remove(self):
        machine = Machine.objects.get(title='Troester', lower='troester', register=123)
        user = User.objects.get(first_name='Anton', telegram_id=123456789)
        Loop.objects.create(machine=machine, user=user)
        telegram_id = 123456789
        cmd = {'cmd': 'loop', 'name': 'troester', 'date': None, 'param': None}  # date, name, cmd, param
        result_test = 'Из Вашего списка отслеживания удалено:\n /troester\n'
        self.assertEqual(display_loop(telegram_id, cmd), result_test)

    def test_list_pure(self):
        telegram_id = 123456789
        cmd = {'cmd': 'loop', 'name': None, 'date': None, 'param': None}
        result_test = 'У Вас еще не выбрано оборудования для отслеживания!'
        self.assertEqual(display_loop(telegram_id, cmd), result_test)
        pass

    def test_list(self):
        machine = Machine.objects.get(title='Troester', lower='troester', register=123)
        user = User.objects.get(first_name='Anton', telegram_id=123456789)
        Loop.objects.create(machine=machine, user=user)
        telegram_id = 123456789
        cmd = {'cmd': 'loop', 'name': None, 'date': None, 'param': None}
        result_test = 'Список отслеживаемого Вами оборудования:\n\n/Troester\n\n'
        self.assertEqual(display_loop(telegram_id, cmd), result_test)

    def test_bad_name(self):
        telegram_id = 123456789
        cmd = {'cmd': 'loop', 'name': 'proton', 'date': None, 'param': None}
        result_test = 'Не найдено оорудование с указанным именем!'
        self.assertEqual(display_loop(telegram_id, cmd), result_test)
