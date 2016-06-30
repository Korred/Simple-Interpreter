import py

from simpleparser import parse
from objmodel import W_NormalObject
from interpreter import Interpreter

def test_primitive():
    ast = parse("""
k = 10 $int_add(31)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("k").value == 41

def test_primitive_mul():
    ast = parse("""
k = 3 $int_mul(4,6)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("k").value == 72

def test_primitive_div():
    ast = parse("""
k = 100 $int_div(10)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("k").value == 10


def test_loop():
    ast = parse("""
def f(x):
    r = 0
    while x:
        r = r $int_add(x)
        x = x $int_add(-1)
    r
y = f(100)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("y").value == 5050

