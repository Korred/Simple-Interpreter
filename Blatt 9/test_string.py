import py

from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *
from objmodel import W_String

def test_string_object():
    w1 = W_String("string")
    w2 = W_String("gnirts")
    assert w1.value == "string"
    assert w2.value == "gnirts"
    assert w1.value == w2.reverse()
    assert w1.append(W_String(w2.reverse())) == "stringstring"

def test_interpreter_builtin_string():
    ast = parse("""
a = "dyn"
b = "lang"
c = " "
d = "20"
e = "16"
la = a len
ab = a append(b)
abc = ab append(c)
de = d append(e)
abcde = abc append(de)
lde = de len
labcde = abcde len
arev = a reverse
abrev = ab reverse
equal = a equals(a)
notequal = a equals(b)
arevrev = a reverse reverse
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").value == "dyn"
    assert w_module.getvalue("b").value == "lang"
    assert w_module.getvalue("c").value == " "
    assert w_module.getvalue("d").value == "20"
    assert w_module.getvalue("e").value == "16"
    assert w_module.getvalue("ab").value == "dynlang"
    assert w_module.getvalue("abc").value == "dynlang "
    assert w_module.getvalue("de").value == "2016"
    assert w_module.getvalue("abcde").value == "dynlang 2016"
    assert w_module.getvalue("arev").value == "nyd"
    assert w_module.getvalue("abrev").value == "gnalnyd"
    assert w_module.getvalue("equal").value == 'True'
    assert w_module.getvalue("notequal").value == 'False'
    assert w_module.getvalue("la").value == 3
    assert w_module.getvalue("lde").value == 4
    assert w_module.getvalue("labcde").value == 12
    assert w_module.getvalue("arevrev").value == "dyn"

def test_interpreter_string_logic():
    ast = parse("""
s = 'test123'
bcond = True
if bcond and(s equals(s reverse reverse)):
    dict = {'a':'test123','b':'test012'}
bool = s equals(dict get('a'))
srev = s reverse reverse
b1 = s equals(s reverse reverse)
b2 = bcond and(s equals(s reverse reverse))
if s equals('123'):
    b3 = True
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("dict").getelement('a').value == "test123"
    assert w_module.getvalue("bool").value == 'True'
    assert w_module.getvalue("srev").value == "test123"
    assert w_module.getvalue("b1").value == 'True'
    assert w_module.getvalue("b2").value == 'True'
    assert w_module.getvalue("b3") == None
