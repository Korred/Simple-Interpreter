import random
import pytest
from collections import deque
# FYI: Run only specific test - for example: py.test -q -s blatt02.py::test_stack_list


# AUFGABE 1
def compute_word_occurences(text):
    words = text.split()
    nest = dict()
    for i in range(len(words)):
        if i+1 < len(words):
            curr = words[i]
            foll = words[i+1]
            if curr not in nest:
                nest[curr] = dict()
            if foll not in nest[curr]:
                nest[curr][foll] = 0
            nest[curr][foll] += 1
    return nest


def make_random_text(nest, num):
    start = random.choice(list(nest.keys()))
    random_text = [start]

    for i in range(num-1):
        d = nest[random_text[i]]
        if d:  # check if dict for given word is not empty
            max_word = max(d.keys(), key=lambda k: d[k])  # lambda function to define key for max
            random_text.append(max_word)
        else:
            break
    return " ".join(random_text)


# AUFGABE 3
# Mutability of common python types:

# The following are immutable objects:
#    Numeric types: int, float, complex
#    string
#    tuple
#    frozen set
#    bytes

# The following objects are mutable:
#    list
#    dict
#    set
#    byte array

# 3.1
def test_stack_list():
    stack = [1, 2, 3]

    # push/add element to stack top
    stack.append(4)
    assert stack == [1, 2, 3, 4]

    # pop/remove element from stack top
    assert stack.pop() == 4
    assert stack == [1, 2, 3]

    # inspect topmost element (last-in)
    assert stack[-1] == 3

    # inspect topmost element will throw IndexError if list/stack is empty
    stack = []
    with pytest.raises(IndexError):
        stack[-1]


# 3.2
def test_queue_deque():
    # Deques are a generalization of stacks and queues
    # (the name is pronounced “deck” and is short for “double-ended queue”)
    deq = deque([1, 2, 3])

    # push/add element from the right
    deq.append(4)
    assert list(deq) == [1,2,3,4]

    # push/add element from the left
    deq.appendleft(4)
    assert list(deq) == [4,1,2,3,4]

    # pop/remove element from the right
    assert deq.pop() == 4
    assert list(deq) == [4,1,2,3]

    # pop/remove element from the right
    assert deq.popleft() == 4
    assert list(deq) == [1,2,3]

    # deque can be bounded - will overwrite/replace elements on the opposite side of append
    deq = deque([],5)
    for i in range(20):
        deq.append(i)
    assert list(deq) == [15,16,17,18,19]
