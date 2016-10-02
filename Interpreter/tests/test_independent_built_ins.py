import sys
sys.path.append("..")
from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *

def test_interpreter_gcd():
    ast = parse("""
a = gcd(14,7)
b = gcd(613,412)
c = gcd(1212,123)
d = gcd(44,4444)
e = gcd(1623,123243)
f = gcd(12064,534)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value == 7
    assert w_module.getvalue("b").value == 1
    assert w_module.getvalue("c").value == 3
    assert w_module.getvalue("d").value == 44
    assert w_module.getvalue("e").value == 3
    assert w_module.getvalue("f").value == 2

def test_interpreter_is_prime():
    ast = parse("""
a = isPrime(3)
b = isPrime(12)
c = isPrime(127)
d = isPrime(248)
e = isPrime(1103)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value is True
    assert w_module.getvalue("b").value is False
    assert w_module.getvalue("c").value is True
    assert w_module.getvalue("d").value is False
    assert w_module.getvalue("e").value is True
