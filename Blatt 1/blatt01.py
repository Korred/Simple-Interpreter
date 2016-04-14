

def count_lines_and_words(file):
    with open(file, "r") as data:
        lines = data.readlines()                                # store lines as a list
        lines_num = len(lines)                                  # length of list == number of lines
        word_num = sum([len(line.split()) for line in lines])   # example: sum([2,2,2,2]) == 8
        return lines_num, word_num                              # return result


def find_zero(f, a, b):
    a, b = sorted([a, b])
    if not ((f(a) < 0 and f(b) > 0) or (f(a) > 0 and f(b) < 0)):
        error_data = [a, str(f(a)), b, str(f(b))]
        raise ValueError('f({0})={1} and f({2})={3} have the same signs!'.format(*error_data))
    else:
        while abs(a-b) >= 0.0001:
            c = 0.5*(a+b)
            if f(c) == 0:
                break
            elif f(a)*f(c) < 0:  # only possible if different signs are present -> c is closer to 0 than b
                b = c
            else:                # same signs present -> c is closer to 0 than a
                a = c
        return 0.5*(a+b)         # not using c as it might be possible to omit the while loop


def approximate_sqrt(num):
    if num < 0:
        raise ValueError('Provided number ({}) is negative!'.format(num))
    else:
        def f(x): return x**2-num
        if num == 0:
            return 0
        else:
            return find_zero(f, 0, num+1)


def make_function(func):
    def f(x):
        exec("from math import *")
        return eval(func)
    return f


def find_zero_from_string(f, a, b):
    return find_zero(make_function(f), a, b)


# AUFGABE 3


def burrows_wheeler_forward(data):
    # sorted() is stable
    rot = sorted([data[i:]+data[:i] for i in range(len(data))])
    code = "".join([r[-1] for r in rot])
    pos = rot.index(data)
    return (code, pos)


def burrows_wheeler_backward(code, pos):
    # sort() is stable
    rot = ['']*len(code)
    for i in range(len(code)):
        for x, c in enumerate(code):
            rot[x] = c + rot[x]
        rot.sort()
    return rot[pos]
