import py

from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *
from objmodel import W_Float, W_Integer

# Lexer Tests


def test_lex_list_int():
    s = "[1,2,3,4,5,6]"
    tokens = lex(s)
    print([t.name for t in tokens])


def test_lex_list_float():
    s = "[1.0,-2.0,3.123,0.0000,-5.125,-0.000]"
    tokens = lex(s)
    print([t.name for t in tokens])


def test_lex_list_string():
    s = """["a","v","z",'i','j','choochoo']"""
    tokens = lex(s)
    print([t.name for t in tokens])


def test_lex_list_mixed():
    s = """[1,2,3.0,-4.2,'2',"abc"]"""
    tokens = lex(s)
    print([t.name for t in tokens])

def test_lex_list_in_list():
    s = """[[1,2,3],[4,5,6]]"""
    tokens = lex(s)
    print([t.name for t in tokens])

# Parser Tests

def test_list_simple_expression():
    ast = parse("[1,2]")
    res = Program([ExprStatement(ListLiteral([IntLiteral(1), IntLiteral(2)]))])

    assert ast == res

def test_list_simple_assignment():
    ast = parse ("a = [1,2]")
    res = Program([Assignment(ImplicitSelf(), 'a', ListLiteral([IntLiteral(1), IntLiteral(2)]))])

    assert ast == res

def test_list_simple_primitive():
    ast = parse("[1] $add(2)")
    res = Program([ExprStatement(PrimitiveMethodCall(ListLiteral([IntLiteral(1)]), '$add', [IntLiteral(2)]))])

    assert ast == res
