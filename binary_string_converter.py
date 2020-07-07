import numpy as np

get_bin = lambda x, n: format(x, 'b').zfill(n)

def int_to_binary_string(number, bits):
    return get_bin(number,bits)


def binary_string_to_int(binary_string):
    print(binary_string)
    print(type(binary_string))
    return int(binary_string, 2)

def nparray_binary_to_int(binary_nparray):
    binary_arr = []
    for i in binary_nparray:
        if i > 0.5:
            binary_arr.append('1')
        else:
            binary_arr.append('0')
    binary_string = "".join(binary_arr)
    return int(binary_string, 2)