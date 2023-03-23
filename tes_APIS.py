import pytest
import unittest
import requests
from ddt import ddt, data, unpack
from parameterized import parameterized

def sum_test(input1, input2):
    return input1 + input2

@ddt
class MyTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setUp(self, input_total):
        pass

    # @data((1,1,2),(1,2,3),(1,3,5))
    # @unpack
    # def test_get(self, input1, input2, expected):
    #     self.assertEqual(input1+input2,expected)

    @parameterized.expand([(1,2,3),(1,3,4)],ids=[("Valus"),("values")])
    def test_get(self, input1, input2, expected):
        value = sum_test(input1, input2)
        self.assertEqual(value, expected)


