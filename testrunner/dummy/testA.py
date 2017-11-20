import unittest

from time import sleep


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        sleep(20)
        self.assertEqual('foo'.upper(), 'FOO')
