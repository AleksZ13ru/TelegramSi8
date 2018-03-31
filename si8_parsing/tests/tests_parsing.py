import os

from django.test import TestCase
from si8_parsing.tests.parsing_file_result import parsing_result
from si8_parsing.code.parsing import parsing_file


class OpenFileSi8TestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_openfilesi8_v2(self):
        result = parsing_result
        name = '300318-8-20.SI8'
        path = os.getcwd() + '/si8_parsing/tests/'
        self.maxDiff = None
        self.assertEqual(parsing_file(path, name), result)
