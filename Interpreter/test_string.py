from simpleparser import parse
from interpreter import Interpreter
from simpleast import *
from objmodel import W_String

def test_parser_string():
    ast = parse("""
s = "text"
if s equals("text"):
    s2 = "profit"
else:
    s2 = "aaaah"
""")
    assert ast == Program([
        Assignment(ImplicitSelf(), 's', StringLiteral('"text"')), 
        IfStatement(MethodCall(
            MethodCall(ImplicitSelf(), 's', []), 'equals', [StringLiteral('"text"')]), 
        Program([Assignment(ImplicitSelf(), 's2', StringLiteral('"profit"'))]), 
        Program([Assignment(ImplicitSelf(), 's2', StringLiteral('"aaaah"'))]))])

    ast = parse("""
a = "text"
s = a reverse
sub = s substring(0,2)
""")
    assert ast == Program([
        Assignment(ImplicitSelf(), 'a', StringLiteral('"text"')), 
        Assignment(ImplicitSelf(), 's', MethodCall(
            MethodCall(ImplicitSelf(), 'a', []), 'reverse', [])), 
        Assignment(ImplicitSelf(), 'sub', MethodCall(
            MethodCall(ImplicitSelf(), 's', []), 'substring', [IntLiteral(0), IntLiteral(2)]))])

    ast = parse("""
s1 = "text"
s2 = "wup"
concat = s1 append(s2)
""")
    assert ast == Program([
        Assignment(ImplicitSelf(), 's1', StringLiteral('"text"')),
        Assignment(ImplicitSelf(), 's2', StringLiteral('"wup"')),
        Assignment(ImplicitSelf(), 'concat', MethodCall(
            MethodCall(ImplicitSelf(), 's1', []), 'append', [MethodCall(ImplicitSelf(), 's2', [])]))])

def test_string_object():
    w1 = W_String("string")
    w2 = W_String("gnirts")
    assert w1.value == "string"
    assert w2.value == "gnirts"
    assert w1.value == w2.reverse()
    assert w1.append(W_String(w2.reverse())) == "stringstring"
    assert w1.equals(w1) is True

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
f = a append("")
g = a append(" ")
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
    assert w_module.getvalue("f").value == "dyn"
    assert w_module.getvalue("g").value == "dyn "


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
c = b reverse
la = a len
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("la").value == 16
    assert w_module.getvalue("a").value == "{[ <'string'> ]}"
    assert w_module.getvalue("b").value == "?!§$%&&%&1234[]{]}"
    assert w_module.getvalue("c").value == "}]{][4321&%&&%$§!?"

def test_interpreter_string_reverse():
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

def test_interpreter_string_equals():
    ast = parse("""
s1 = "test"
s2 = "test1"
s3 = "test "
s4 = "test"
b1 = s1 equals(s1)
b2 = s1 equals(s2)
b3 = s2 equals(s3)
b4 = s1 equals(s3)
b5 = s1 equals(s4)
b6 = "" equals(" ")
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("b1").value is True
    assert w_module.getvalue("b2").value is False
    assert w_module.getvalue("b3").value is False
    assert w_module.getvalue("b4").value is False
    assert w_module.getvalue("b5").value is True
    assert w_module.getvalue("b6").value is False

def test_interpreter_string_logic():
    ast = parse("""
s = 'test123'
if True and(s equals(s reverse reverse)):
    dict = {'a':'test123','b':'test012'}
bool = s equals(dict get('a'))
srev = s reverse reverse
b1 = s equals(s reverse reverse)
b2 = False or(s equals(s reverse reverse))
if s equals('123'):
    b3 = True
else:
    b3 = False
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("dict").getelement('a').value == "test123"
    assert w_module.getvalue("bool").value is True
    assert w_module.getvalue("srev").value == "test123"
    assert w_module.getvalue("b1").value is True
    assert w_module.getvalue("b2").value is True
    assert w_module.getvalue("b3").value is False


def test_interpreter_string_substring():
    ast = parse("""
s1 = "test"
s2 = "das ist ein test"
sub1 = s1 substring(0,1)
sub2 = s1 substring(1,3)
sub3 = s1 substring(2,1)
sub4 = s2 substring(4,11)
sub5 = s2 substring(12,20)
sub6 = "" substring(0,5)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("sub1").value == "t"
    assert w_module.getvalue("sub2").value == "es"
    assert w_module.getvalue("sub3").value == ""
    assert w_module.getvalue("sub4").value == "ist ein"
    assert w_module.getvalue("sub5").value == "test"
    assert w_module.getvalue("sub6").value == ""


def test_interpreter_string_in_string():
    ast = parse("""
quote1 = "'as'"
quote2 = '"as"'
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("quote1").value == "'as'"
    assert w_module.getvalue("quote2").value == '"as"'
