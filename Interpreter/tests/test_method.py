import sys
sys.path.append("..")
from simpleparser import parse
from interpreter import Interpreter


def test_method_simple_int():
    ast = parse("""
object a:
    x = 11
    def f:
        self x
object b:
    __parent__ = a
    x = 22
af = a f # a is the receiver, therefore self is a in the method
bf = b f # b is the receiver, therefore self is b in the method

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("af").value == 11
    assert w_module.getvalue("bf").value == 22


def test_method_simple_float():
    ast = parse("""
object a:
    x = 13.37
    def f:
        self x
object b:
    __parent__ = a
    x = 4.04
af = a f # a is the receiver, therefore self is a in the method
bf = b f # b is the receiver, therefore self is b in the method

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("af").value == 13.37
    assert w_module.getvalue("bf").value == 4.04


def test_method_simple_string():
    ast = parse("""
object a:
    x = "string"
    def f:
        self x
object b:
    __parent__ = a
    x = "string"
af = a f # a is the receiver, therefore self is a in the method
bf = b f # b is the receiver, therefore self is b in the method

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("af").value == "string"
    assert w_module.getvalue("bf").value == "string"


def test_method_simple_bool():
    ast = parse("""
object a:
    x = True
    def f:
        self x
object b:
    __parent__ = a
    x = False
af = a f # a is the receiver, therefore self is a in the method
bf = b f # b is the receiver, therefore self is b in the method

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("af").value is True
    assert w_module.getvalue("bf").value is False


def test_method_simple_list():
    ast = parse("""
object a:
    x = [1,2]
    def f:
        self x
object b:
    __parent__ = a
    x = [3,4]
af = a f # a is the receiver, therefore self is a in the method
bf = b f # b is the receiver, therefore self is b in the method

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert [i.value for i in w_module.getvalue("af").elements] == [1, 2]
    assert [i.value for i in w_module.getvalue("bf").elements] == [3, 4]


def test_method_simple_dict():
    ast = parse("""
object a:
    x = {1:2}
    def f:
        self x
object b:
    __parent__ = a
    x = {3:4}
af = a f # a is the receiver, therefore self is a in the method
bf = b f # b is the receiver, therefore self is b in the method

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    d1 = w_module.getvalue("af")
    d2 = w_module.getvalue("bf")
    assert d1.getelement(1).value == 2
    assert d2.getelement(3).value == 4


def test_method_complex_int():
    ast = parse("""
k = 10
object a:
    x = 11
    y = 22
    def f(a, b):
        if a:
            if b:
                a
            else:
                k
        else:
            if b:
                self x
            else:
                self y
object b:
    __parent__ = a
    y = 55
af11 = a f(1, 1)
af10 = a f(1, 0)
af01 = a f(0, 1)
af00 = a f(0, 0)
k = 908
bf11 = b f(1, 1)
bf10 = b f(1, 0)
bf01 = b f(0, 1)
bf00 = b f(0, 0)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("af11").value == 1
    assert w_module.getvalue("af10").value == 10
    assert w_module.getvalue("af01").value == 11
    assert w_module.getvalue("af00").value == 22
    assert w_module.getvalue("bf11").value == 1
    assert w_module.getvalue("bf10").value == 908
    assert w_module.getvalue("bf01").value == 11
    assert w_module.getvalue("bf00").value == 55
