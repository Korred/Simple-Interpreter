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
    ast = parse("a = [1,2]")
    res = Program([Assignment(ImplicitSelf(), 'a', ListLiteral([IntLiteral(1), IntLiteral(2)]))])

    assert ast == res


def test_list_simple_primitive():
    ast = parse("[1] $add(2)")
    res = Program([ExprStatement(PrimitiveMethodCall(ListLiteral([IntLiteral(1)]), '$add', [IntLiteral(2)]))])

    assert ast == res


def test_list_empty():
    ast = parse("[]")
    res = Program([ExprStatement(ListLiteral([]))])

    assert ast == res


# Interpreter Tests

def test_list_i_simple():
    ast = parse("""
a = [1,2,3,4]
b = [-1.555,0.0,+1.5,5]
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    for i in range(4):
        assert w_module.getvalue("a").elements[i].value == i+1

    assert type(w_module.getvalue("b").elements[0].value) == type(-1.555)
    assert type(w_module.getvalue("b").elements[1].value) == type(0.0)
    assert type(w_module.getvalue("b").elements[2].value) == type(+1.5)
    assert type(w_module.getvalue("b").elements[3].value) == type(5)

    assert w_module.getvalue("b").elements[0].value == -1.555
    assert w_module.getvalue("b").elements[1].value == 0.0
    assert w_module.getvalue("b").elements[2].value == +1.5
    assert w_module.getvalue("b").elements[3].value == 5


def test_list_i_def():
    ast = parse("""
def o:
    [1,2,3,4]
a = o
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    for i in range(4):
        assert w_module.getvalue("a").elements[i].value == i+1


def test_list_i_inlist():
    ast = parse("""
a = [[1,2,3,4],[5,6,7,8]]
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert [e.value for e in w_module.getvalue("a").elements[0].elements] == [1,2,3,4]
    assert [e.value for e in w_module.getvalue("a").elements[1].elements] == [5,6,7,8]


def test_list_i_add():
    ast = parse("""
a = []
a add(1)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").elements[0].value == 1