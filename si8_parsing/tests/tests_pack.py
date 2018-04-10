from django.test import TestCase
from datetime import datetime

from si8_parsing.code.pack import repack


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
                  '  средняя: 11 м/мин. \n',
                  '  макс.: 12.36 м/мин. в 00:48 \n',
                  'Всего: 124 м.\n\n',
                  '00:00 - 00:02 = 32 м.\n',
                  '00:42 - 00:49 = 92 м.\n']

        name = 'Troester'
        d = datetime(2018, 3, 30, 7, 30).date()
        inputs = [11.33, 12.36, 8.24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9.27, 12.36, 11.33, 12.36, 11.33, 11.33, 12.36, 11.33]
        self.assertEqual(repack(name, d, inputs), result)

    def test_repack_2(self):
        result = ['Оборудование: /Troester\n',
                  'Дата: 30 March 2018\n',
                  'Остановов: 1 \n',
                  'Скорость:\n',
                  '  средняя: 2 м/мин. \n',
                  '  макс.: 2.00 м/мин. в 00:09 \n',
                  'Всего: 9 м.\n\n',
                  '00:00 - 00:02 = 3 м.\n',
                  '00:07 - 00:09 = 6 м.\n']

        name = 'Troester'
        d = datetime(2018, 3, 30, 7, 30).date()
        inputs = [1, 1, 1, 0, 0, 0, 0, 2, 2, 2]
        self.assertEqual(repack(name, d, inputs), result)

    def test_repack_3(self):
        result = ['Оборудование: /Troester\n',
                  'Дата: 30 March 2018\n',
                  'Остановов: 1 \n',
                  'Скорость:\n',
                  '  средняя: 1 м/мин. \n',
                  '  макс.: 2.00 м/мин. в 00:07 \n',
                  'Всего: 10 м.\n\n',
                  '00:00 - 00:02 = 3 м.\n',
                  '00:05 - 00:08 = 7 м.\n']

        name = 'Troester'
        d = datetime(2018, 3, 30, 7, 30).date()
        inputs = [1, 1, 1, 0, 0, 2, 2, 2, 1]
        self.assertEqual(repack(name, d, inputs), result)

    def test_repack_4(self):
        result = ['Оборудование: /Troester\n',
                  'Дата: 30 March 2018\n',
                  'Остановов: 0 \n',
                  'Скорость:\n',
                  '  средняя: 1 м/мин. \n',
                  '  макс.: 2.00 м/мин. в 00:06 \n',
                  'Всего: 9 м.\n\n',
                  '00:00 - 00:06 = 9 м.\n']

        name = 'Troester'
        d = datetime(2018, 3, 30, 7, 30).date()
        inputs = [1, 1, 1, 0, 2, 2, 2]
        self.assertEqual(repack(name, d, inputs), result)
