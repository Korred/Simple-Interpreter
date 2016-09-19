from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *
from objmodel import W_Float, W_Integer

# Lexer Tests


def test_lex_float():
    for s in ["0.0", "0.555", "1.0", "1.1", "+1.1", "-1.0", "-2.1234567890"]:
        tokens = lex(s)
        assert tokens[0].name == 'Float'


# Parser Tests


def test_par_float():
    pass


# objmodel Tests


def test_obj_float():
    w1 = W_Float(5.0)    # should be a float
    w2 = W_Integer(5.0)  # should be an int
    assert isinstance(w1.value, float)
    assert isinstance(w2.value, int)
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
    # the constructor is called without arguments
    # so the default builtins are used instead
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
    assert w_module.getvalue("fi").value == w_module.getvalue("ci").value == 5


def test_int_float_compare():
    ast = parse("""
i1 = 5
i2 = 0
i3 = -5

f1 = 7.5
f2 = 7.4
f3 = -2.3

e1 = i1 equals(5)           # True
e2 = f3 equals(-2.3)        # True
e3 = i2 equals(f2)          # False

lt1 = i3 less_than(i1)      # True
lt2 = f3 less_than(f2)      # True
lt3 = i3 less_than(f3)      # True
lt4 = f3 less_than(i3)      # False

le1 = i3 less_equal(i3)     # True
le2 = i3 less_equal(i1)     # True
le3 = f3 less_equal(f2)     # True
le4 = f3 less_equal(i1)     # True
le5 = f3 less_equal(i3)     # False

gt1 = i1 greater_than(i2)   # True
gt2 = i3 greater_than(i1)   # False
gt3 = f1 greater_than(f2)   # True
gt4 = f3 greater_than(f2)   # False
gt5 = i1 greater_than(f3)   # True

ge1 = i1 greater_equal(i2)  # True
ge2 = i2 greater_equal(0)   # True
ge3 = i3 greater_equal(i1)  # False
ge4 = f1 greater_equal(f2)  # True
ge5 = f3 greater_equal(i1)  # False
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("e1").value is True
    assert w_module.getvalue("e2").value is True
    assert w_module.getvalue("e3").value is False

    assert w_module.getvalue("lt1").value is True
    assert w_module.getvalue("lt2").value is True
    assert w_module.getvalue("lt3").value is True
    assert w_module.getvalue("lt4").value is False

    assert w_module.getvalue("le1").value is True
    assert w_module.getvalue("le2").value is True
    assert w_module.getvalue("le3").value is True
    assert w_module.getvalue("le4").value is True
    assert w_module.getvalue("le5").value is False

    assert w_module.getvalue("gt1").value is True
    assert w_module.getvalue("gt2").value is False
    assert w_module.getvalue("gt3").value is True
    assert w_module.getvalue("gt4").value is False
    assert w_module.getvalue("gt5").value is True

    assert w_module.getvalue("ge1").value is True
    assert w_module.getvalue("ge2").value is True
    assert w_module.getvalue("ge3").value is False
    assert w_module.getvalue("ge4").value is True
    assert w_module.getvalue("ge5").value is False


def test_int_float_compare_err1():
    ast = parse("""
s = "string"
f = 1.5

err = f greater_than(s)

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    py.test.raises(TypeError, interpreter.eval, ast, w_module)


def test_int_float_compare_err2():
    ast = parse("""
l = [1,2,3,4]
f = 1.5

err = f less_than(l)

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    py.test.raises(TypeError, interpreter.eval, ast, w_module)


def test_int_float_compare_err3():
    ast = parse("""
d = {1:2}
f = 1.5

err = f greater_equal(d)

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    py.test.raises(TypeError, interpreter.eval, ast, w_module)

def test_float_int_sqrt():
    ast = parse("""
a = 5.0 sqrt
b = 4 sqrt
c = 144 sqrt
d = 1021 sqrt
e = 0 sqrt
f = 23.12 sqrt
g = 162.21 sqrt
h = 102.002 sqrt
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value == 2.23606797749979
    assert w_module.getvalue("b").value == 2.0
    assert w_module.getvalue("c").value == 12.0
    assert w_module.getvalue("d").value == 31.953090617340916
    assert w_module.getvalue("e").value == 0.0
    assert w_module.getvalue("f").value == 4.8083261120685235
    assert w_module.getvalue("g").value == 12.736168968728391
    assert w_module.getvalue("h").value == 10.099603952631014

def test_int_modulo():
    ast = parse("""
a = 2 mod(2)
b = 122 mod(3)
c = 65 mod(432)
d = 128 mod(2)
e = 61261 mod(72)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value == 0
    assert w_module.getvalue("b").value == 2
    assert w_module.getvalue("c").value == 65
    assert w_module.getvalue("d").value == 0
    assert w_module.getvalue("e").value == 61
