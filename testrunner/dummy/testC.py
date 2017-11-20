import unittest


class SecondTestClass(unittest.TestCase):

    def setUp(self):
        self.val = 210

    def test_sub(self):
        self.val = 210
        self.assertEquals(210, self.val)
        self.val = self.val - 40
        self.assertEquals(170, self.val)

    def test_mul(self):
        self.val = 210
        self.assertEquals(420, self.val * 2)
