import py
from blatt02 import *
# AUFGABE 1

def test_word_occurences():
    d = compute_word_occurences("a b a b a c a c")
    assert d == {
        "a": {"b": 2, "c": 2},
        "b": {"a": 2},
        "c": {"a": 1}
    }

def test_word_occurences_long():
    with open('faust1.txt', encoding='utf-8') as f:
        s = f.read()
    d = compute_word_occurences(s)
    assert d["_Faust._"]["Habe"] == 1
    assert d["Habe"]["nun,"] == 1
    assert d["nun,"]["ach!"] == 1
    assert d["_Gretchen._"] == {
        '(nach': 1,
        '(steckt': 1,
        'Ach!': 1,
        'Allmächtiger!': 1,
        'Das': 2,
        'Er': 1,
        'Kein': 1,
        'Mein': 2,
        'Mir': 1,
        'Nachbarin!': 1,
        'Weh!': 1,
        'Wie': 1,
        'Wär’': 1,
        }


def test_random_words():
    with open('faust1.txt', encoding='utf-8') as f:
        s = f.read()
    d1 = compute_word_occurences(s)
    text = make_random_text(d1, 100)
    d2 = compute_word_occurences(text)
    last = None
    for word in text.split():
        if last is not None:
            assert word in d1[last]
        last = word
    print(text)

# AUFGABE 2

class A(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def f(self, z):
        return self.x + self.y + z


class B(A):
    def g(self):
        return self.x * 17


def test_send():
    a = A(12, 13)
    assert a.f(1) == 26
    assert send(a, "f", 1) == 26

    b = B(14, 15)
    assert b.f(-1) == 28
    assert send(b, "f", -1) == 28
    assert b.g() == 14 * 17
    assert send(b, "g") == 14 * 17


def test_send_not_found():
    a = A(12, 13)
    py.test.raises(AttributeError, "a.notthere(1)")
    py.test.raises(AttributeError, "send(a, 'notthere', 1)")


class C(A):
    def message_not_understood(self, message, *args):
        return ('we have seen', message, args)


def test_send_message_not_understood():
    c = C(16, 17)
    assert send(c, 'notthere', 1) == ('we have seen', 'notthere', (1,))

# Aufgabe 3
# Aufgabe 3.1 - Stack

def test_push():
    pass #xxx implement me

def test_pop():
    pass #xxx implement me

# Aufgabe 3.2 - Queue

def test_enqueue():
    pass #xxx implement me

def test_dequeue():
    pass #xxx implement me

# Aufgabe 3.3

# Hint: towers are zero indexed

def test_hanoi_3():
    towers = hanoi(3)
    assert towers[0][-1] == 1
    assert towers[0][-2] == 2
    assert towers[0][-3] == 3
    move(towers,0,2)
    move(towers,0,1)
    move(towers,2,1)
    move(towers,0,2)
    move(towers,1,0)
    move(towers,1,2)
    move(towers,0,2)
    assert towers[2][-1] == 1
    assert towers[2][-2] == 2
    assert towers[2][-3] == 3

def test_hanoi_4():
    towers = hanoi(4)
    assert towers[0][-1] == 1
    assert towers[0][-2] == 2
    assert towers[0][-3] == 3
    assert towers[0][-4] == 4
    move(towers,0,1)
    move(towers,0,2)
    move(towers,1,2)
    move(towers,0,1)
    move(towers,2,0)
    move(towers,2,1)
    move(towers,0,1)
    move(towers,0,2)
    move(towers,1,2)
    move(towers,1,0)
    move(towers,2,0)
    move(towers,1,2)
    move(towers,0,1)
    move(towers,0,2)
    move(towers,1,2)
    assert towers[2][-1] == 1
    assert towers[2][-2] == 2
    assert towers[2][-3] == 3
    assert towers[2][-4] == 4
