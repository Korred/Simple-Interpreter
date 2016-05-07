import py

from blatt04 import *

# Aufgabe 1 - Huffman Coding

def test_make_coding():
    freq = {"a": 1, "b": 2, "c": 5, "d": 18}
    tree = make_tree(freq)
    assert tree.right.value == "d"
    assert tree.left.right.value == "c"
    assert tree.left.left.right.value == "b"
    assert tree.left.left.left.value == "a"


def test_mapping():
    freq = {"a": 1, "b": 2, "c": 5, "d": 18}
    tree = make_tree(freq)
    mapping = make_mapping(tree)
    assert mapping["a"] == "000"
    assert mapping["b"] == "001"
    assert mapping["c"] == "01"
    assert mapping["d"] == "1"


def test_encode():
    freq = {"a": 1, "b": 2, "c": 5, "d": 18}
    tree = make_tree(freq)
    mapping = make_mapping(tree)
    s = encode(mapping, "ddaccddb")
    assert s == "11000010111001"


def test_decode():
    freq = {"a": 1, "b": 2, "c": 5, "d": 18}
    tree = make_tree(freq)
    s = decode(tree, "1010001010110100101000101")
    assert s == "dcadccdcbcadc"

# Aufgabe 2

def test_hashset():
    l = [None] * 5
    hashinsert(l, 3456)
    assert hashcontains(l, 3456)
    assert not hashcontains(l, 456)

    hashinsert(l, 456)
    assert hashcontains(l, 456)


def test_hashset_collision_detection():
    l = [None] * 5
    hashinsert(l, 1)
    hashinsert(l, 6)
    assert hashcontains(l, 1)
    assert hashcontains(l, 6)


def test_hashset_insert_twice():
    l = [None] * 5
    hashinsert(l, 1)
    assert hashcontains(l, 1)
    hashinsert(l, 1)
    assert hashcontains(l, 1)


def hashinsert(l, value):
    pos = value % len(l)

    while l[pos] is not None:
        pos += 1
    l[pos] = value


def hashcontains(l, value):
    pos = value % len(l)

    while l[pos] is not None:
        if l[pos] == value:
            return True
        pos += 1
    return False
