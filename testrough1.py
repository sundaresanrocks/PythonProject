def diff_odd_even(input):
    sum_even = 0
    sum_odd = 0
    for i in input:
        if i%2 == 0:
            sum_even = sum_even + i

        else:
            sum_odd = sum_odd + i

    return sum_even - sum_odd

# input = [1, 2, 3, 4, 5]
# imput1 = [1, 2, 3, 4, 5]
# input2 = [4,21,3,2,3,10]
# input3 = [1,3,2,2,2,2,2]
#
# difference = diff_odd_even(input3)
# print(difference)

def decorator(func):
    def inner1(*args, **kwargs):
        return_value = func(*args, **kwargs)
            

def decorator_sum_two_number(func):
    def inner1(*args, **kargs):
        print("computing Sum")
        return_value = func(*args, **kargs)
        return return_value
    return inner1

def decorator_sum_two_number_modifier(func):
    def inner1(*args, **kargs):
        return_value = func(*args, **kargs)
        if return_value % 2 != 0:
            print("Not an even number, so adding 1")
            return_value += 1
        return return_value
    return inner1



@decorator_sum_two_number
@decorator_sum_two_number_modifier
def sum_two_number(a, b):
    return a+b

sum_call = sum_two_number(2,3)
print(sum_call)