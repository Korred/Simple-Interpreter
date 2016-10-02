import sys
import py
sys.path.append("..")
from simpleparser import parse
from interpreter import Interpreter


def test_builtin_simple():
    builtincode = """
x = 1
object None:
    1
def pass:
    None
"""
    # construct the builtin module by running builtincode within the context of
    # a new empty module
    interpreter = Interpreter(builtincode)
    w_module = interpreter.make_module()
    # the parent of a normal module is the builtin module
    builtins = w_module.getparents()[0]
    assert builtins.getvalue('x').value == 1

    ast = parse("""
tx = x
object a:
    pass
ax = a x
""")
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("ax").value == 1
    assert w_module.getvalue("tx").value == 1


def test_inttrait():
    builtincode = """
object inttrait:
    x = 1
    def maybe_fortytwo:
        if self:
            42
        else:
            x
"""
    interpreter = Interpreter(builtincode)
    w_module = interpreter.make_module()
    # the parent of a normal module is the builtin module
    builtins = w_module.getparents()[0]
    inttrait = builtins.getvalue("inttrait")

    ast = parse("""
x = 5 x # this returns 1, because it looks in the inttrait defined above
m0 = 0 maybe_fortytwo
m1 = x maybe_fortytwo
inttrait x = 2
m2 = 0 maybe_fortytwo
tr = inttrait
""")
    interpreter.eval(ast, w_module)
    x = w_module.getvalue("x")
    assert w_module.getvalue("tr") is inttrait
    # the inttrait is defined in the builtin module, so its __parent__ is that
    # module
    assert inttrait.getparents() == [builtins]
    assert x.value == 1
    assert x.getparents() == [inttrait]
    assert w_module.getvalue("m0").value == 1
    assert w_module.getvalue("m1").value == 42
    assert w_module.getvalue("m2").value == 2


def test_builtin_default():
    ast = parse("""
def sumupto(x):
    r = 0
    while x:
        r = r add(x)
        x = x add(-1)
    r
x = sumupto(100)
""")
    # the constructor is called without arguments, so the default builtins are
    # used
    interpreter = Interpreter()
    # test that the default inttrait defines a method ``add``
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("x").value == 5050


def test_builtin_convert():
    ast = parse("""
a = 1
b = 2.5
c = "string"
d = -1.5
e = +2.2

a1 = to_int(a)
a2 = to_float(a)
a3 = to_str(a)

b1 = to_int(b)
b2 = to_float(b)
b3 = to_str(b)

c1 = to_str(c)

d1 = to_int(d)
d2 = to_float(d)
d3 = to_str(d)

e1 = to_int(e)
e2 = to_float(e)
e3 = to_str(e)

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("a1").value == 1
    assert w_module.getvalue("a2").value == 1.0
    assert w_module.getvalue("a3").value == "1"

    assert w_module.getvalue("b1").value == 2
    assert w_module.getvalue("b2").value == 2.5
    assert w_module.getvalue("b3").value == "2.5"

    assert w_module.getvalue("c1").value == "string"

    assert w_module.getvalue("d1").value == -1
    assert w_module.getvalue("d2").value == -1.5
    assert w_module.getvalue("d3").value == "-1.5"

    assert w_module.getvalue("e1").value == 2
    assert w_module.getvalue("e2").value == 2.2
    assert w_module.getvalue("e3").value == "2.2"


def test_builtin_convert_err_a():
    ast = parse("""
c = "string"
c1 = to_int(c) # will not work
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    py.test.raises(ValueError, interpreter.eval, ast, w_module)


def test_builtin_convert_err_b():
    ast = parse("""
c = "string"
c2 = to_float(c) # will not work
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    py.test.raises(ValueError, interpreter.eval, ast, w_module)
