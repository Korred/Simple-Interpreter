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

def test_interpreter_boolean():
    ast = parse("""
a = True
if a:
    b = {'a':1,'b':2,'c':3}
else:
    b = {'a':10,'b':11,'c':12}
c = b get('a')
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("a").value == 'True'
    assert w_module.getvalue("c").value == 1