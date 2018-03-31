import os

from django.test import TestCase
from si8_parsing.code2 import get_hash_md5


class Code2TestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_get_hash_md5(self):
        result = '85bf926c4efa0b9ca0e1b96d20ad1398'
        name = '300318-8-20.SI8'
        path = os.getcwd() + '/si8_parsing/tests/'
        self.maxDiff = None
        self.assertEqual(get_hash_md5(path, name), result)

    def test_get_hash_md5_none(self):
        name = 'pure.SI8'
        path = os.getcwd()
        self.maxDiff = None
        self.assertEqual(get_hash_md5(path, name), None)
