from simpleparser import parse
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


def test_interpreter_string_append():
    ast = parse("""
a = "dyn"
b = "lang"
c = " "
d = "20"
e = "16"
ab = a append(b)
abc = ab append(c)
de = d append(e)
abcde = abc append(de)
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


def test_interpreter_string_length():
    ast = parse("""
a = "string"
b = "laaaaaaaaaaaanger string"
c = ""
d = " "
la = a len
lb = b len
lc = c len
ld = d len
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("la").value == 6
    assert w_module.getvalue("lb").value == 24
    assert w_module.getvalue("lc").value == 0
    assert w_module.getvalue("ld").value == 1


def test_interpreter_string_special_signs():
    ast = parse("""
a = "{[ <'string'> ]}"
b = "?!§$%&&%&1234[]{]}"
la = a len
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("la").value == 16
    assert w_module.getvalue("a").value == "{[ <'string'> ]}"
    assert w_module.getvalue("b").value == "?!§$%&&%&1234[]{]}"


def test_interpreter_builtin_string():
    ast = parse("""
a = "dynlang"
b = "gnalnyd"
arev = a reverse
brev = b reverse
emptyrev = "" reverse
equal1 = a equals(brev)
equal2 = arev equals(b)
arevrev = a reverse reverse
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("arev").value == "gnalnyd"
    assert w_module.getvalue("brev").value == "dynlang"
    assert w_module.getvalue("emptyrev").value == ""
    assert w_module.getvalue("equal1").value is True
    assert w_module.getvalue("equal2").value is True
    assert w_module.getvalue("arevrev").value == "dynlang"


def test_interpreter_string_logic():
    ast = parse("""
s = 'test123'
bcond = True
if bcond and(s equals(s reverse reverse)):
    dict = {'a':'test123','b':'test012'}
bool = s equals(dict get('a'))
srev = s reverse reverse
b1 = s equals(s reverse reverse)
b2 = False or(s equals(s reverse reverse))
if s equals('123'):
    b3 = True
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("dict").getelement('a').value == "test123"
    assert w_module.getvalue("bool").value is True
    assert w_module.getvalue("srev").value == "test123"
    assert w_module.getvalue("b1").value is True
    assert w_module.getvalue("b2").value is True
    assert w_module.getvalue("b3") is None
