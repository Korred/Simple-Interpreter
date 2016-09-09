import py

from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *

def test_parser_boolean():
    ast = parse("""
a = True
b = False
if a:
    c = True
""")
    assert ast == Program([Assignment(ImplicitSelf(), 'a', BoolLiteral('True')), Assignment(ImplicitSelf(), 'b', BoolLiteral('False')), IfStatement(MethodCall(ImplicitSelf(), 'a', []), Program([Assignment(ImplicitSelf(), 'c', BoolLiteral('True'))]), None)])

    ast = parse("""
a = {1:True,2:False,3:True}
b = [True,False,False,True]
""")
    assert ast == Program([Assignment(ImplicitSelf(), 'a', DictLiteral([KeyValueLiteral(IntLiteral(1), BoolLiteral('True')), KeyValueLiteral(IntLiteral(2), BoolLiteral('False')), KeyValueLiteral(IntLiteral(3), BoolLiteral('True'))])), Assignment(ImplicitSelf(), 'b', ListLiteral([BoolLiteral('True'), BoolLiteral('False'), BoolLiteral('False'), BoolLiteral('True')]))])

    ast = parse("""
a = True
b = a not
c = a or(b)
d = b and(b)
""")
    assert ast == Program([Assignment(ImplicitSelf(), 'a', BoolLiteral('True')), Assignment(ImplicitSelf(), 'b', MethodCall(MethodCall(ImplicitSelf(), 'a', []), 'not', [])), Assignment(ImplicitSelf(), 'c', MethodCall(MethodCall(ImplicitSelf(), 'a', []), 'or', [MethodCall(ImplicitSelf(), 'b', [])])), Assignment(ImplicitSelf(), 'd', MethodCall(MethodCall(ImplicitSelf(), 'b', []), 'and', [MethodCall(ImplicitSelf(), 'b', [])]))])

def test_interpreter_boolean():
    ast = parse("""
a = True
if a:
    b = {'a':1,'b':2,'c':3}
else:
    b = {'a':10,'b':11,'c':12}
c = b get('a')
neg = False
bool1 = neg not
bool2 = a and(bool1)
bool3 = neg and(neg)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("a").value == True
    assert w_module.getvalue("neg").value == False
    assert w_module.getvalue("bool1").value == True
    assert w_module.getvalue("bool2").value == True
    assert w_module.getvalue("bool3").value == False
    assert w_module.getvalue("c").value == 1

def test_interpreter_boolean_logic():
    ast = parse("""
a = True
b = False
c = a and(b or(a))
d = a and(a not)
e = a nand(a)
f = a nor(a)
g = a xnor(b xor(b nand(e)))
h = a nand(e or(g nor(a)))
i = h and(g) not
j = a and(b xor(b nand(a nand(e or(g nor(a or(e xor(g nor(a)))) not)))))
k = a not not
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("c").value == True
    assert w_module.getvalue("d").value == False
    assert w_module.getvalue("e").value == False
    assert w_module.getvalue("f").value == False
    assert w_module.getvalue("g").value == True
    assert w_module.getvalue("h").value == True
    assert w_module.getvalue("i").value == False
    assert w_module.getvalue("j").value == True
    assert w_module.getvalue("k").value == True
