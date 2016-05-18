# Aufgabe 1 - Generators
from blatt06 import *

# Aufgabe 1.1 - TreeNode

def test_tree1():
    tree1 = TreeNode(5, TreeNode(3, TreeNode(1, None,
                                                TreeNode(2, None,
                                                            None)),
                                    TreeNode(4, None,
                                                None)),
                        TreeNode(7, TreeNode(6, None,
                                                None),
                                    TreeNode(8, None,
                                                TreeNode(9, None,
                                                            None))))
    assert list(tree1.enumerate()) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(tree1.enumerate_first()) == [5, 3, 1, 2, 4, 7, 6, 8, 9]
    assert list(tree1.enumerate_last()) == [2, 1, 4, 3, 6, 9, 8, 7, 5]

# Aufgabe 1.2 - Square root

import math

def test_sqrt_from_0():
    gen = sqrt_gen(0)
    for i,s in zip(range(10),gen):
        assert s == math.sqrt(i)

def test_sqrt_from_3000000():
    gen = sqrt_gen(3000000)
    for i,s in zip(range(3000000,3040000),gen):
        assert s == math.sqrt(i)

# Aufgabe 1.3 - Permutations

def test_permutations_1():
    assert list(permute("a")) == ["a"]

def test_permutations_2():
    assert list(permute("ab")) == ["ab", "ba"]

def test_permutations():
    text = "abcd"
    permutations = permute(text)
    result = ["abcd", "bacd", "cabd", "dabc", "abdc", "badc", "cadb", "dacb",
              "acbd", "bcad", "cbad", "dbac", "acdb", "bcda", "cdba", "dbca",
              "adbc", "bdac", "cdab", "dcab", "adcb", "bdca", "cbda", "dcba"]
    assert sorted(list(permutations)) == sorted(result)

# Aufgabe 2

# write tests here

# Aufgabe 3/4

SQUARE = set([(0,0), (0,1),
              (1,0), (1,1)])

def test_from_life_string():
    assert from_lifestring("") == set()
    assert from_lifestring("X") == set([(0,0)])
    assert from_lifestring("X X") == set([(0, 0), (2, 0)])

    assert from_lifestring("XX\nXX") == SQUARE
    assert from_lifestring("XX\nX ") == set([(0,0), (0,1), (1,0)])
