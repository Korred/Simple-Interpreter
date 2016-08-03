import py

from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *
from objmodel import W_Float, W_Integer

# Lexer Tests


def test_lex_float_regexp():
    pass


def test_lex_float():
    for s in ["0.0", "0.555", "1.0", "1.1", "+1.1", "-1.0", "-2.1234567890"]:
        tokens = lex(s)
        assert tokens[0].name == 'Float'


# Parser Tests


def test_par_float():
    pass


# AST Tests


def test_ast_float():
    pass


# objmodel Tests


def test_obj_float():
    w1 = W_Float(5.0)    # should be a float
    w2 = W_Integer(5.0)  # should be an int
    assert w1.value == 5.0
    assert w2.value == 5
    # W_Float objects cannot have custom attributes,
    # so getvalue() returns None.
    assert w1.getvalue('abc') is None
    assert w2.getvalue('abc') is None


# Interpreter Tests


def test_simple_float():
    ast = parse("""
a = 5.2
b = 0.0
c = -0.0
d = +0.0
e = -5.5
f = 5.555555555555555555555550000
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value == 5.2
    assert w_module.getvalue("b").value == 0.0
    assert w_module.getvalue("c").value == 0.0
    assert w_module.getvalue("d").value == 0.0
    assert w_module.getvalue("e").value == -5.5
    assert w_module.getvalue("f").value == 5.55555555555555555555555

def test_float_primitives():
    ast = parse("""
x = 10
y = 2.0

sum1 = x add(y)
dif1 = x sub(y)
prod1 = x mul(y)
quot1 = x div(y)

x = 2.0
y = 10

sum2 = x add(y)
dif2 = x sub(y)
prod2 = x mul(y)
quot2 = x div(y)
""")
    # the constructor is called without arguments, so the default builtins are used
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("sum1").value == 12.0
    assert w_module.getvalue("dif1").value == 8.0
    assert w_module.getvalue("prod1").value == 20.0
    assert w_module.getvalue("quot1").value == 5.0

    assert w_module.getvalue("sum2").value == 12.0
    assert w_module.getvalue("dif2").value == -8.0
    assert w_module.getvalue("prod2").value == 20.0
    assert w_module.getvalue("quot2").value == 0.2

def test_float_if():
    ast = parse("""
x = 0.0 #0.0 is false but can be changed if needed
y = 1.0

if x:
    x = 1.0
if y:
    y = 2.0
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("x").value == 0.0
    assert w_module.getvalue("y").value == 2.0

def test_float_floor_ceil():
    ast = parse("""
x = 5.5
y = 5
ff = floor(x)
cf = ceil(x)
fi = floor(y)
ci = ceil(y)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("ff").value == 5.0
    assert w_module.getvalue("cf").value == 6.0
    print(w_module.getvalue("ff").value, w_module.getvalue("cf").value)
    print(w_module.getvalue("fi").value, w_module.getvalue("ci").value)
