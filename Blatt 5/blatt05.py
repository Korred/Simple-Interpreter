'''
Aufgabe 1 - Descriptors
Using the descriptor protocol (see the Lecture), re-implement Python's classmethod and staticmethod built-in functions. Write tests as necessary.
'''
# A descriptor is an object with any of the following methods (__get__, __set__, or __delete__), 
# intended to be used via dotted-lookup as if it were a typical attribute of an instance
#
# classmethod and staticmethod are Non-Data-Descriptors
'''
A Data Descriptor has a __set__ and/or __delete__.
A Non-Data-Descriptor has neither __set__ nor __delete__.
'''


class myclassmethod(object):
    # instance = Object instance
    # cls = Owner Class
    def __init__(self, funct):
        self.funct = funct

    def __get__(self, instance, cls):
        # print("self: ", self); print("instance: ", instance); print("cls: ", cls)

        def classfunc(*args):
            return self.funct(cls, *args)

        return classfunc


class mystaticmethod(object):
    def __init__(self, funct):
        self.funct = funct

    def __get__(self, instance, cls):
        return self.funct

'''
Aufgabe 2 - More Descriptors
Using descriptors implement object attributes that validate values on assignment. The test functions are given in test_blatt04.py.
The IntField class is used to represent integers. It has a default value which can be overwritten. The value will always be casted into an integer if possible.
The RangeField class represents a range-style object. It has two values for the start and the end of the range (end excluded). The end needs to be greater than the start.
'''


class IntField(object):
    def __init__(self, name, value=0):
        self.name = name
        self.value = int(value)

    def __get__(self, instance, cls):
        if self.name not in instance.__dict__:
            return self.value
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, val):
        instance.__dict__[self.name] = int(val)

# remember a.i means check attribute i in class of a FIRST!


class RangeField(object):

    def __init__(self, name, start=0, end=1):
        self.name = name

        if start < end:
            self.start = start
            self.end = end
        else:
            raise ValueError()

    def __get__(self, instance, cls):
        if self.name not in instance.__dict__:
            return self.end
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, val):
        # val ist hier das end-range
        s = self.start
        if s < val:
            instance.__dict__[self.name] = val
        else:
            raise ValueError()

'''
Aufgabe 3
'''


def mybin(integer):
    if integer == 0:
        return "0"
    else:
        bin = []
        while integer > 0:
            if (round(integer) & 1) == 0:
                bin = ["0"] + bin      # append to front, because we need to read bits backwards
            else:
                bin = ["1"] + bin
            integer = integer // 2
        bin = ["0b"] + bin
        return "".join(bin)


def myint(bin_string):
    cut_string = bin_string[2:][::-1]
    length = len(cut_string)
    int = 0
    i = 0
    while i < length:
        expo = length - i - 1
        if cut_string[expo] == '1':
            int += 2**expo
        i += 1
    return int
