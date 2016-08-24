import py

from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *

# Lexer Tests

def test_lexer():
    s = "{\"a\":1,\"b\":2}"
    tokens = lex(s)
    assert [t.name for t in tokens] == ['MapOpenBracket', 'String', 'Colon', 'Number', 'Comma', 'String', 'Colon', 'Number', 'MapCloseBracket', 'Newline', 'EOF']

    s = "{4:\"a\"}"
    tokens = lex(s)
    assert [t.name for t in tokens] == ['MapOpenBracket', 'Number', 'Colon', 'String', 'MapCloseBracket', 'Newline', 'EOF']

    s = "{1:4.3}"
    tokens = lex(s)
    assert [t.name for t in tokens] == ['MapOpenBracket', 'Number', 'Colon', 'Float', 'MapCloseBracket', 'Newline', 'EOF']

# Parser Tests

def test_parser_simple_dict():
    ast = parse("{1:1,1:2}")
    assert ast == Program([ExprStatement(DictLiteral([KeyValueLiteral(IntLiteral(1), IntLiteral(1)), KeyValueLiteral(IntLiteral(1), IntLiteral(2))]))])

    ast = parse("a = {1:\"a\",2:\"b\"}")
    assert ast == Program([Assignment(ImplicitSelf(), 'a', DictLiteral([KeyValueLiteral(IntLiteral(1), StringLiteral('"a"')), KeyValueLiteral(IntLiteral(2), StringLiteral('"b"'))]))])

    ast = parse("""
a = {12:\"a\",27:\"b\"}
b = {\"a\":2,\"b\":4}
""")
    assert ast == Program([Assignment(ImplicitSelf(), 'a', DictLiteral([KeyValueLiteral(IntLiteral(12), StringLiteral('"a"')), KeyValueLiteral(IntLiteral(27), StringLiteral('"b"'))])), Assignment(ImplicitSelf(), 'b', DictLiteral([KeyValueLiteral(StringLiteral('"a"'), IntLiteral(2)), KeyValueLiteral(StringLiteral('"b"'), IntLiteral(4))]))])


def test_parser_builtin_dict():
    ast = parse("{\"a\":1,\"b\":2} add(\"c\",4)")
    assert ast == Program([ExprStatement(MethodCall(DictLiteral([KeyValueLiteral(StringLiteral('"a"'), IntLiteral(1)), KeyValueLiteral(StringLiteral('"b"'), IntLiteral(2))]), 'add', [StringLiteral('"c"'), IntLiteral(4)]))])

    ast = parse("{\"a\":1,\"b\":2,\"c\":4} del(\"b\")")
    assert ast == Program([ExprStatement(MethodCall(DictLiteral([KeyValueLiteral(StringLiteral('"a"'), IntLiteral(1)), KeyValueLiteral(StringLiteral('"b"'), IntLiteral(2)), KeyValueLiteral(StringLiteral('"c"'), IntLiteral(4))]), 'del', [StringLiteral('"b"')]))])
    
    ast = parse("{\"a\":1,\"b\":2,\"c\":4} get(\"a\")")
    assert ast == Program([ExprStatement(MethodCall(DictLiteral([KeyValueLiteral(StringLiteral('"a"'), IntLiteral(1)), KeyValueLiteral(StringLiteral('"b"'), IntLiteral(2)), KeyValueLiteral(StringLiteral('"c"'), IntLiteral(4))]), 'get', [StringLiteral('"a"')]))])

    ast = parse("""
a = {1:2,2:3}
b = {\"a\":13,\"b\":14}
e = b get(\"b\")
a del(1)
""")
    assert ast == Program([Assignment(ImplicitSelf(), 'a', DictLiteral([KeyValueLiteral(IntLiteral(1), IntLiteral(2)), KeyValueLiteral(IntLiteral(2), IntLiteral(3))])), Assignment(ImplicitSelf(), 'b', DictLiteral([KeyValueLiteral(StringLiteral('"a"'), IntLiteral(13)), KeyValueLiteral(StringLiteral('"b"'), IntLiteral(14))])), Assignment(ImplicitSelf(), 'e', MethodCall(MethodCall(ImplicitSelf(), 'b', []), 'get', [StringLiteral('"b"')])), ExprStatement(MethodCall(MethodCall(ImplicitSelf(), 'a', []), 'del', [IntLiteral(1)]))])


# Interpreter Tests

def test_interpreter_dict():
    ast = parse("a = {\"a\":1,\"b\":2,\"c\":4}")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    dict = w_module.getvalue("a")
    assert dict.getelement("a").value == 1
    assert dict.getelement("b").value == 2
    assert dict.getelement("c").value == 4

def test_interpreter_add_del_dict():
    ast = parse("""
a = {2:1,1:2,3:4}
a del(1)
b = a len
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    dict = w_module.getvalue("a")
    assert dict.getelement(2).value == 1
    assert dict.getelement(3).value == 4
    assert dict.getelement(1) == None
    assert w_module.getvalue("b").value == 2

def test_interpreter_builtin_dict():
    ast = parse("""
condition = True
neg = False
if neg or(condition and(condition)):
    a = {'a':12,'b':11,'c':10}
else:
    a = {'a':12,'b':11,'c':10}
a del('a')
a add('d',9)
a add('e',8)
a add('f',7)
length = a len
value = a get('d')
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("condition").value == 'True'
    assert w_module.getvalue("length").value == 5
    assert w_module.getvalue("value").value == 9

def test_interpreter_mixed_builtin_dict():
    ast = parse("""
a = {\"a\":1.1,\"b\":2.3,\"c\":3.5}
a del(\"a\")
a add(\"d\",4.7)
b = a len
c = a get(\"d\")
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    dict = w_module.getvalue("a")
    assert dict.getelement("b").value == 2.3
    assert dict.getelement("c").value == 3.5
    assert dict.getelement("d").value == 4.7
    assert dict.getelement("a") == None
    assert w_module.getvalue("c").value == 4.7
    assert w_module.getvalue("b").value == 3

def test_interpreter_mixed_keys_dict():
    ast = parse("""
a = {\"a\":1.1,\"b\":2.3,\"c\":3.5,1:\"som\",2:\"eth\",3:\"wupwup\"}
a del(3)
a add(3,\"ing\")
b = a len
contains = a contains(1)
notcontains = a contains(27)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    dict = w_module.getvalue("a")
    assert dict.getelement("a").value == 1.1
    assert dict.getelement("b").value == 2.3
    assert dict.getelement("c").value == 3.5
    assert dict.getelement(1).value == "som"
    assert dict.getelement(2).value == "eth"
    assert dict.getelement(3).value == "ing"
    assert w_module.getvalue("contains").value == True
    assert w_module.getvalue("notcontains").value == False
    assert w_module.getvalue("b").value == 6

def test_interpreter_boolean_dict():
    ast = parse("""
condition1 = True
condition2 = False
condition3 = True
if condition2 or(condition1 and(condition3)):
    dict = {12:True,13:False,32:True}
else:
    dict = {12:False,32:False}
length = dict len
temp = dict get(12)
result = temp not
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    dict = w_module.getvalue("dict")
    assert dict.getelement(12).value == 'True'
    assert w_module.getvalue("temp").value == 'True'
    assert w_module.getvalue("result").value == 'False'
    assert w_module.getvalue("length").value == 3
