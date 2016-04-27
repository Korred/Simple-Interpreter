import py

from blatt03 import *

# AUFGABE 1

def test_mygetattr_override():
    class A(object):
        pass
    register_override(object, "fortytwo", 42)
    register_override(A, "fortyone", 41)
    a = A()
    assert mygetattr(a, "fortytwo") == 42
    assert mygetattr(a, "fortyone") == 41
    assert mygetattr([], "fortytwo") == 42
    py.test.raises(ValueError, mygetattr, 1, "fortyone")

# AUFGABE 2


SQUARE = set([(0, 0), (0, 1),
              (1, 0), (1, 1)])
HLINE = set([(-1, 0), (0, 0), (1, 0)])
VLINE = set([(0, -1), (0, 0), (0, 1)])

GLIDER = set([         (0, -1),
                               (1, 0),
              (-1, 1), (0, 1), (1, 1)])

SHIFTED_GLIDER = set([(x + 1,y + 1) for (x, y) in GLIDER])


def test_life_step():
    assert lifestep(set()) == set()
    assert lifestep(set([(0, 0)])) == set()

    assert lifestep(SQUARE) == SQUARE
    assert lifestep(set([(0, 0), (0, 1),
                         (1, 0)       ])) == SQUARE

    assert lifestep(HLINE) == VLINE
    assert lifestep(VLINE) == HLINE

    assert lifestep(lifestep(lifestep(lifestep(GLIDER)))) == SHIFTED_GLIDER


def test_life_string():
    assert lifestring(set()) == ""
    assert lifestring(set([(0, 0)])) == "X"
    assert lifestring(set([(10, -5),(12, -5)])) == "X X"

    assert lifestring(SQUARE) == "XX\nXX"    # '\n' is an end-of-line character
    assert lifestring(set([(0, 0), (0, 1),
                           (1, 0)       ])) == "XX\nX "

    assert lifestring(HLINE) == "XXX"
    assert lifestring(VLINE) == "X\nX\nX"

    assert lifestring(GLIDER) == (" X \n" +
                                  "  X\n" +
                                  "XXX")
    assert lifestring(SHIFTED_GLIDER) == lifestring(GLIDER)


def test_life_big():
    import time
    state = set([        (0, -1), (1, -1),
                 (-1, 0), (0, 0),
                          (0, 1)          ])
    for i in range(1103):
        # for fun, print the first 100 iterations
        if i < 200:
            print('-'*80)
            print(lifestring(state))
            time.sleep(0.1)
        state = lifestep(state)
    resulting_string = lifestring(state)    # big! about 500x500...

    import hashlib
    h = hashlib.md5(resulting_string.encode("utf-8")).hexdigest()
    assert h == '274cb707b8579bb5a0efbc1b56b0de59'

# Aufgabe 3

def test_open_class():
    class A(object, metaclass=OpenClass):

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def f(self):
            return self.x + self.y

        value = 7

    a = A(2, 4)
    assert a.f() == 6
    assert a.value == 7
    py.test.raises(AttributeError, "a.g()")

    class __enhance__(A):
        value = 9

        def g(self):
            return self.x * self.y

    assert a.value == 9
    assert a.g() == 8
