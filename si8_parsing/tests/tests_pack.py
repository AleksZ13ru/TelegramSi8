from django.test import TestCase
from si8_parsing.code.pack import repack
from si8_parsing.tests.parsing_file_result import parsing_result
from datetime import date


class RepackTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_repack(self):
        result = ['Оборудование: /Troester\n',
                  'Дата: 30 March 2018\n',
                  'Остановов: 1 \n',
                  'Скорость:\n',
                  '  средняя: 10 м/мин. \n',
                  '  макс.: 12.36 м/мин. в 08:18 \n',
                  'Всего: 124 м.\n\n',
                  '07:30 - 07:33 = 32 м.\n',
                  '08:12 - 08:19 = 92 м.\n']

        name = 'Troester'
        r = parsing_result['bufs'][0]
        d = r['now_date'].date()
        inputs = r['value']
        self.assertEqual(repack(name, d, inputs), result)
