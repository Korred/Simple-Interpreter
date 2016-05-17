from blatt05 import *
import py

# Aufgabe 1

def test_classmethod():
    class A(object):
        i = 0

        def f(cls):
            cls.i += 1
        f = myclassmethod(f)

    A.f()
    assert A.i == 1
    a = A()
    a.f()
    assert A.i == 2
    assert a.i == 2
    a.i = 'a'
    a.f()
    assert A.i == 3
    assert a.i == 'a'


def test_staticmethod():
    class A(object):
        def f(i):
            return i
        f = mystaticmethod(f)

    assert A.f('a') == 'a'
    a = A()
    assert a.f(34) == 34
    assert a.f(a) is a

# Aufgabe 2

def make_class():
    class A(object):
        i = IntField("i")
        j = IntField("j", 10)
    return A


def test_type_validation_defaults():
    A = make_class()
    a = A()

    assert a.i == 0
    assert a.j == 10


def test_type_validation():
    A = make_class()
    a = A()
    a.i = 1
    assert a.i == 1
    a.i = 2.1
    assert a.i == 2
    a.i = "123"
    assert a.i == 123


def test_type_validation_different_instances():
    A = make_class()

    a = A()
    a.i = 1

    b = A()
    assert b.j == 10
    assert b.i == 0

    assert a.i == 1
    assert a.j == 10


def make_range_field_class():
    class A(object):
        i = RangeField('i', 5, 10)
    return A


def test_range_validation():
    A = make_range_field_class()
    a = A()
    a.i = 6
    assert a.i == 6
    with py.test.raises(ValueError):
        a.i = 0


def test_different_instances():
    A = make_range_field_class()
    a = A()
    a = A()
    a.i = 6
    #
    b = A()
    assert b.i != 6


def test_invalid_range():
    with py.test.raises(Exception):
        class B(object):
            j = RangeField('j', 5, 1)

# Aufgabe 3

import random

def test_int_to_bin():
    input = random.sample(range(1000), 10)
    for x in input:
        assert mybin(x) == bin(x)

def test_bin_to_int():
    input = [(i, bin(i)) for i in random.sample(range(1000), 10)]
    for i, bini in input:
        assert myint(bini) == i
