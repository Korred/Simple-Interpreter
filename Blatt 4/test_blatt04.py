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

# insertion to full hashset failed, because while condition looped until element is None
# therefore index out of bounds error
def test_insert_to_full_hashset():
    l = [1,2,3,4]
    assert hashinsert(l,5)
    assert hashcontains(l,5)

def test_empty_hashset():
    l = []
    # hashcontains crashed for empty sets
    assert hashcontains(l,1) == False
    # no insertion to empty set
    hashinsert(l,1)
    assert l == []

def hashinsert(l, value):
    length = len(l)
    if (length != 0):
        pos = value % length

        while pos < length-1:
            if(l[pos] is None):
                break
            else:
                pos += 1
        # override first hashed position if hashset is full
        if((pos == length-1) & (l[pos] is None)):
            l[pos] = value
        else:
            l[value%length] = value

def hashcontains(l, value):
    length = len(l)
    if (length == 0):
        return False
    else:
        pos = value % length

        while l[pos] is not None:
            if l[pos] == value:
                return True
            pos += 1
        return False