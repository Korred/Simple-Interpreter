import sys
sys.path.append("..")
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
    assert ast == Program([
        Assignment(ImplicitSelf(), 'a', BoolLiteral('True')), 
        Assignment(ImplicitSelf(), 'b', BoolLiteral('False')), 
        IfStatement(MethodCall(ImplicitSelf(), 'a', []), 
            Program([Assignment(ImplicitSelf(), 'c', BoolLiteral('True'))]), None)])

    ast = parse("""
a = {1:True,2:False,3:True}
b = [True,False,False,True]
""")
    assert ast == Program([
        Assignment(ImplicitSelf(), 'a', 
            DictLiteral([
                KeyValueLiteral(IntLiteral(1), BoolLiteral('True')), 
                KeyValueLiteral(IntLiteral(2), BoolLiteral('False')), 
                KeyValueLiteral(IntLiteral(3), BoolLiteral('True'))])), 
        Assignment(ImplicitSelf(), 'b', 
            ListLiteral([
                BoolLiteral('True'), 
                BoolLiteral('False'), 
                BoolLiteral('False'), 
                BoolLiteral('True')]))])

    ast = parse("""
a = True
b = a not
c = a or(b)
d = b and(b)
""")
    assert ast == Program([
        Assignment(ImplicitSelf(), 'a', BoolLiteral('True')), 
        Assignment(ImplicitSelf(), 'b', 
            MethodCall(MethodCall(ImplicitSelf(), 'a', []), 'not', [])), 
        Assignment(ImplicitSelf(), 'c', 
            MethodCall(MethodCall(ImplicitSelf(), 'a', []), 'or', 
                [MethodCall(ImplicitSelf(), 'b', [])])), 
        Assignment(ImplicitSelf(), 'd', 
            MethodCall(MethodCall(ImplicitSelf(), 'b', []), 'and', 
                [MethodCall(ImplicitSelf(), 'b', [])]))])

def test_interpreter_boolean_if():
    ast = parse("""
if True and(True or(True not)):
    b = {'a':1,'b':2,'c':3}
else:
    b = {'a':10,'b':11,'c':12}
c = b get('a')
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("c").value == 1

def test_interpreter_boolean_and():
    ast = parse("""
b1 = True and(False)
b2 = True and(True)
b3 = True and(False and(True))
b4 = True and(True and(True))
b5 = b2 and(b4)
b6 = True nand(False)
b7 = False nand(True and(False))
b8 = True nand(True)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("b1").value is False
    assert w_module.getvalue("b2").value is True
    assert w_module.getvalue("b3").value is False
    assert w_module.getvalue("b4").value is True
    assert w_module.getvalue("b5").value is True
    assert w_module.getvalue("b6").value is True
    assert w_module.getvalue("b7").value is True
    assert w_module.getvalue("b8").value is False

def test_interpreter_boolean_or():
    ast = parse("""
b1 = True or(False)
b2 = True or(True)
b3 = True or(False or(True nor(False)))
b4 = False or(True nor(True))
b5 = b2 or(b4)
b6 = False nor(True)
b7 = False nor(False)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("b1").value is True
    assert w_module.getvalue("b2").value is True
    assert w_module.getvalue("b3").value is True
    assert w_module.getvalue("b4").value is False
    assert w_module.getvalue("b5").value is True
    assert w_module.getvalue("b6").value is False
    assert w_module.getvalue("b7").value is True

def test_interpreter_boolean_exclusive():
    ast = parse("""
b1 = True xor(True)
b2 = False xor(False)
b3 = True xor(False xnor(True or(False)))
b4 = False or(True xnor(True))
b5 = b2 xnor(b4)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("b1").value is False
    assert w_module.getvalue("b2").value is False
    assert w_module.getvalue("b3").value is True
    assert w_module.getvalue("b4").value is True
    assert w_module.getvalue("b5").value is False

def test_interpreter_boolean_implication():
    ast = parse("""
b1 = True impl(False)
b2 = False impl(True)
b3 = True and(True) impl(False nand(False nand(False or(True nor(False)))))
b4 = False impl(False)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("b1").value is False
    assert w_module.getvalue("b2").value is True
    assert w_module.getvalue("b3").value is True
    assert w_module.getvalue("b4").value is True

def test_interpreter_boolean_equals():
    ast = parse("""
b1 = True equals(False)
b2 = True equals(True)
b3 = False equals(True and(True) not)
b4 = False or(True) nand(False or(True)) equals(True)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("b1").value is False
    assert w_module.getvalue("b2").value is True
    assert w_module.getvalue("b3").value is True
    assert w_module.getvalue("b4").value is False

def test_interpreter_boolean_combined():
    ast = parse("""
a = True
b = False
c = a and(b or(a))
d = a and(a not)
e = a xnor(b xor(b nand(a nand(a))))
f = a nand(a nand(a or(e nor(a))))
g = f and(e) not
h = a and(b xor(b nand(a nand(a nand(a or(e nor(a or(a nand(a) xor(e nor(a)))) not))))))
i = a not not
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("c").value is True
    assert w_module.getvalue("d").value is False
    assert w_module.getvalue("e").value is True
    assert w_module.getvalue("f").value is True
    assert w_module.getvalue("g").value is False
    assert w_module.getvalue("h").value is True
    assert w_module.getvalue("i").value is True
