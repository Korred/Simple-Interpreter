import py
import pytest
from blatt07 import *

# Aufgabe 2 - Special Methods
def burrows_wheeler_forward(s):
    strings = []
    for i in range(len(s)):
        strings.append(s[i:] + s[:i])
    strings.sort()
    i = strings.index(s)
    output = ''.join([s[-1] for s in strings])
    return (output, i)


def test_forward_transformation():
    # see http://de.wikipedia.org/wiki/Burrows-Wheeler-Transformation
    assert burrows_wheeler_forward("TEXTUEL") == ("UTELXTE", 3)

    input = ("TRENTATRE.TRENTINI.ANDARONO.A.TRENTO"
             ".TUTTI.E.TRENTATRE.TROTTERELLANDO")
    expected_output = ("OIIEEAEO..LDTTNN.RRRRRRRTNTTLE"
                       "AAIOEEEENTRDRTTETTTTATNNTTNNAAO....OU.T")
    assert burrows_wheeler_forward(input) == (expected_output, 60)


# Aufgabe 3 - Proxies

import sys
__bool__ = '__bool__' if sys.version_info > (3,) else '__nonzero__'

def test_logging_proxy_simple():
    class A(object):
        def __init__(self, a):
            self.a = a

        def f(self, x):
            result = self.a
            self.a = x
            return result

    a = A(1)
    p = LoggingProxy(a)
    assert p.a == 1
    attr = p.f(10)
    assert attr == 1
    assert p.a == 10
    assert get_proxy_log(p) == ["a", "f", "a"]

def test_logging_proxy_special():
    p = LoggingProxy(41.0)
    assert p + 2 == 43.0
    assert p - 2 == 39.0
    assert p == 41.0
    assert p
    assert p * 2 == 82.0
    assert p // 2 == 20.0
    assert p > 1.0
    assert get_proxy_log(p) == ["__add__", "__sub__", "__eq__", __bool__,
                                "__mul__", "__floordiv__", "__gt__"]
