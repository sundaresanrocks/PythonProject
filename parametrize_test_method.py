import pytest


def foo(a):
    return a + 1


# import pytest
#
# @pytest.mark.parametrize("test_input,expected", [(4, 8), (4, 8), (4, 8)])
# def test_eval(test_input, expected):
#     assert test_input*2 == expected
#
@pytest.mark.parametrize("a,b,c",[(1,1,2),(2,2,4),(3,3,6)])
def test_parametrization(a,b,c):
    assert a+b == c

def uppercase_decorator(function):
    def wrapper(arg1):
        func = function(arg1)
        upper_case = func.upper()
        return upper_case
    return wrapper

@uppercase_decorator
def say_hi(a):
    return a

s = say_hi("hello")
print(s)