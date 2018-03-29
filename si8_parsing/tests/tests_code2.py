from django.test import TestCase
from si8_parsing.models import File
from si8_parsing.code2 import parsing_si8


class ParsingSi8TestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        File.objects.create(name='010318.SI8', path='/home/aleksz/PycharmProjects/DataSi8/0318/')
        pass

    def setUp(self):
        pass

    def test_parsing_si8(self):
        result = None
        self.assertEqual(parsing_si8(), result)
