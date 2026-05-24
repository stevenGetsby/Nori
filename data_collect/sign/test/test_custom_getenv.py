# -*- coding: utf-8 -*-


import os
import unittest

from data_collect.sign.pkg.utils import custom_getenv


class TestCustomGetenv(unittest.TestCase):

    def setUp(self):
        os.environ['TEST_INTEGER'] = '123'
        os.environ['TEST_FLOAT'] = '123.45'
        os.environ['TEST_BOOLEAN'] = 'true'
        os.environ['TEST_STRING'] = '"Hello, World!"'
        os.environ['TEST_LIST'] = '[1, 2, 3]'
        os.environ['TEST_DICT'] = '{"key": "value"}'
        os.environ['TEST_INVALID_JSON'] = 'invalid json'

    def tearDown(self):
        del os.environ['TEST_INTEGER']
        del os.environ['TEST_FLOAT']
        del os.environ['TEST_BOOLEAN']
        del os.environ['TEST_STRING']
        del os.environ['TEST_LIST']
        del os.environ['TEST_DICT']
        del os.environ['TEST_INVALID_JSON']

    def test_custom_getenv_integer(self):
        self.assertEqual(custom_getenv('TEST_INTEGER'), 123)

    def test_custom_getenv_float(self):
        self.assertEqual(custom_getenv('TEST_FLOAT'), 123.45)

    def test_custom_getenv_boolean(self):
        self.assertEqual(custom_getenv('TEST_BOOLEAN'), True)

    def test_custom_getenv_string(self):
        self.assertEqual(custom_getenv('TEST_STRING'), "Hello, World!")

    def test_custom_getenv_list(self):
        self.assertEqual(custom_getenv('TEST_LIST'), [1, 2, 3])

    def test_custom_getenv_dict(self):
        self.assertEqual(custom_getenv('TEST_DICT'), {"key": "value"})

    def test_custom_getenv_invalid_json(self):
        self.assertEqual(custom_getenv('TEST_INVALID_JSON'), 'invalid json')

    def test_custom_getenv_default(self):
        self.assertEqual(custom_getenv('NON_EXISTENT_KEY', 'default_value'), 'default_value')

if __name__ == '__main__':
    unittest.main()
