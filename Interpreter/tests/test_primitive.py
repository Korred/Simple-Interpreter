import sys
sys.path.append("..")
from simpleparser import parse
from interpreter import Interpreter


def test_primitive():
    ast = parse("""
a = 10 $int_add(31)
b = 10 $int_add(10,10,10)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value == 41
    assert w_module.getvalue("b").value == 40


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
a = 100 $int_div(10)
b = 2 $int_div(4) # 0.5 but should be 0 as we are looking at ints

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value == 10
    assert w_module.getvalue("b").value == 0


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
