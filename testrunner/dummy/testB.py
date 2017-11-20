import unittest

from time import sleep


class TestStringMethods(unittest.TestCase):
    def test_lower(self):
        sleep(20)
        self.assertEqual('GooD'.lower(), 'GOOD')
