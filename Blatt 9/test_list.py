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

def test_list_length():
    ast = parse("""
a = [1,2,3,4]
a del(1)
l1 = a len
a add(5)
a add(6)
l2 = a len
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("l1").value == 3
    assert w_module.getvalue("l2").value == 5

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
a add([1])
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").elements[0].value == 1
    assert w_module.getvalue("a").elements[1].elements[0].value == 1


def test_list_i_del():
    ast = parse("""
a = [1,2,3]
b = [1,2,3]
c = [1,2,3]
a del(0) #first
b del(1) #middle
c del(2) #last
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert [e.value for e in w_module.getvalue("a").elements] == [2,3]
    assert [e.value for e in w_module.getvalue("b").elements] == [1,3]
    assert [e.value for e in w_module.getvalue("c").elements] == [1,2]
    assert w_module.getvalue("a").length == w_module.getvalue("b").length == w_module.getvalue("c").length == 2


def test_list_i_append():
    ast = parse("""
a = [1,2]
b = [3,4]
c = a append(b)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    for i in range(4):
        assert w_module.getvalue("c").elements[i].value == i+1


def test_list_i_range():
    ast = parse("""
s = s_range(5)
e = e_range(5,10)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    for i in range(5):
        assert w_module.getvalue("s").elements[i].value == i
    for i in range(5,10):
        assert w_module.getvalue("e").elements[i-5].value == i

def test_list_i_fibonacci():
    ast = parse("""
f = fibonacci_iter(6)

def fib_list(x):
    r = []
    i = 0
    k = x add(1)

    while k:
        f = fibonacci_iter(i)
        r add(f)
        i = i add(1)
        k = k sub(1)
    r

l = fib_list(6)

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("f").value == 8
    assert [e.value for e in w_module.getvalue("l").elements] == [0,1,1,2,3,5,8]