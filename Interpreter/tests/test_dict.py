import sys
sys.path.append("..")
from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *

# Lexer Tests


def test_lexer():
    s = "{'a':1,'b':2}"
    tokens = lex(s)
    res = ['MapOpenBracket', 'String', 'Colon',
           'Number', 'Comma', 'String', 'Colon',
           'Number', 'MapCloseBracket', 'Newline',
           'EOF']
    assert [t.name for t in tokens] == res

    s = "{4:'a'}"
    tokens = lex(s)
    res = ['MapOpenBracket', 'Number', 'Colon',
           'String', 'MapCloseBracket', 'Newline',
           'EOF']
    assert [t.name for t in tokens] == res

    s = "{1:4.3}"
    tokens = lex(s)
    res = ['MapOpenBracket', 'Number', 'Colon',
           'Float', 'MapCloseBracket', 'Newline', 'EOF']
    assert [t.name for t in tokens] == res

# Parser Tests


def test_parser_simple_dict():

    ast = parse("{1:1,1:2}")
    p = Program([ExprStatement(
        DictLiteral(
            [KeyValueLiteral(IntLiteral(1), IntLiteral(1)),
             KeyValueLiteral(IntLiteral(1), IntLiteral(2))]
        ))])
    assert ast == p

    ast = parse("a = {1:'a',2:'b'}")
    p = Program([Assignment(
        ImplicitSelf(),
        'a',
        DictLiteral(
            [KeyValueLiteral(IntLiteral(1), StringLiteral('"a"')),
             KeyValueLiteral(IntLiteral(2), StringLiteral('"b"'))]
        ))])
    assert ast == p

    ast = parse("""
a = {12:'a',27:'b'}
b = {'a':2,'b':4}
""")
    p = Program([
                Assignment(
                    ImplicitSelf(),
                    'a',
                    DictLiteral(
                        [KeyValueLiteral(IntLiteral(12), StringLiteral('"a"')),
                         KeyValueLiteral(IntLiteral(27), StringLiteral('"b"'))]
                    )),
                Assignment(
                    ImplicitSelf(),
                    'b',
                    DictLiteral(
                        [KeyValueLiteral(StringLiteral('"a"'), IntLiteral(2)),
                         KeyValueLiteral(StringLiteral('"b"'), IntLiteral(4))]
                    ))])
    assert ast == p


def test_parser_builtin_dict():
    ast = parse("{'a':1,'b':2} add('c',4)")
    p = Program([ExprStatement(
        MethodCall(
            DictLiteral(
                [KeyValueLiteral(StringLiteral('"a"'), IntLiteral(1)),
                 KeyValueLiteral(StringLiteral('"b"'), IntLiteral(2))]
            ),
            'add',
            [StringLiteral('"c"'), IntLiteral(4)]))])
    assert ast == p

    ast = parse("{'a':1,'b':2,'c':4} del('b')")
    p = Program([ExprStatement(
        MethodCall(
            DictLiteral(
                [KeyValueLiteral(StringLiteral('"a"'), IntLiteral(1)),
                 KeyValueLiteral(StringLiteral('"b"'), IntLiteral(2)),
                 KeyValueLiteral(StringLiteral('"c"'), IntLiteral(4))]),
            'del',
            [StringLiteral('"b"')]))])
    assert ast == p

    ast = parse("{'a':1,'b':2,'c':4} get('a')")
    p = Program([ExprStatement(
        MethodCall(
            DictLiteral(
                [KeyValueLiteral(StringLiteral('"a"'), IntLiteral(1)),
                 KeyValueLiteral(StringLiteral('"b"'), IntLiteral(2)),
                 KeyValueLiteral(StringLiteral('"c"'), IntLiteral(4))]),
            'get',
            [StringLiteral('"a"')]))])
    assert ast == p

    ast = parse("""
a = {1:2,2:3}
b = {'a':13,'b':14}
e = b get('b')
a del(1)
""")
    p = Program([
        Assignment(
            ImplicitSelf(),
            'a',
            DictLiteral([
                KeyValueLiteral(IntLiteral(1), IntLiteral(2)),
                KeyValueLiteral(IntLiteral(2), IntLiteral(3))])),
        Assignment(
            ImplicitSelf(),
            'b',
            DictLiteral([
                KeyValueLiteral(StringLiteral('"a"'), IntLiteral(13)),
                KeyValueLiteral(StringLiteral('"b"'), IntLiteral(14))])),
        Assignment(
            ImplicitSelf(),
            'e',
            MethodCall(
                MethodCall(
                    ImplicitSelf(),
                    'b',
                    []),
                'get',
                [StringLiteral('"b"')])),
        ExprStatement(
            MethodCall(
                MethodCall(
                    ImplicitSelf(),
                    'a',
                    []),
                'del',
                [IntLiteral(1)]))])
    assert ast == p

# Interpreter Tests


def test_interpreter_dict():
    ast = parse("a = {'a':1,'b':2,'c':4}")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    d = w_module.getvalue("a")
    assert d.getelement("a").value == 1
    assert d.getelement("b").value == 2
    assert d.getelement("c").value == 4


def test_interpreter_add_del_dict():
    ast = parse("""
m1 = {2:1,1:2,3:4}
m2 = {2.2:12,'z':13,3:14}

m1 del(1)
m2 del(2.2)
m2 del('z')
m1len = m1 len
m2len1 = m2 len
m2 del(3)
m2len2 = m2 len
m2 add(3.2,'abc')

m3 = {}
m3 del(1)
m3 del('a')
m3 del(1.2)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    d = w_module.getvalue("m1")
    assert d.getelement(2).value == 1
    assert d.getelement(3).value == 4
    assert d.getelement(1) is None
    assert w_module.getvalue("m1len").value == 2
    assert w_module.getvalue("m2len1").value == 1
    assert w_module.getvalue("m2len2").value == 0
    assert w_module.getvalue("m2").getelement(3.2).value == 'abc'
    assert w_module.getvalue("m3").elements == {}


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
    assert w_module.getvalue("condition").value is True
    assert w_module.getvalue("length").value == 5
    assert w_module.getvalue("value").value == 9


def test_interpreter_mixed_builtin_dict():
    ast = parse("""
a = {'a':1.1,'b':2.3,'c':3.5}
a del('a')
a add('d',4.7)
b = a len
c = a get('d')
d = {}
d del('a')
d add('a',1.2)
d del('b')
dlen = d len
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    d = w_module.getvalue("a")
    assert d.getelement("b").value == 2.3
    assert d.getelement("c").value == 3.5
    assert d.getelement("d").value == 4.7
    assert d.getelement("a") is None
    assert w_module.getvalue("c").value == 4.7
    assert w_module.getvalue("b").value == 3
    assert w_module.getvalue("d").getelement('a').value == 1.2
    assert w_module.getvalue("dlen").value == 1


def test_interpreter_mixed_keys_dict():
    ast = parse("""
a = {'a':1.1,'b':2.3,'c':3.5,1:'som',2:'eth',3:'wupwup',4.2:'wsws',2.7:3.4}
a del(3)
a add(3,'ing')
b = a len
contains = a contains(1)
notcontains = a contains(27)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    d = w_module.getvalue("a")
    assert d.getelement("a").value == 1.1
    assert d.getelement("b").value == 2.3
    assert d.getelement("c").value == 3.5
    assert d.getelement(1).value == "som"
    assert d.getelement(2).value == "eth"
    assert d.getelement(3).value == "ing"
    assert d.getelement(4.2).value == "wsws"
    assert d.getelement(2.7).value == 3.4
    assert w_module.getvalue("contains").value is True
    assert w_module.getvalue("notcontains").value is False
    assert w_module.getvalue("b").value == 8


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
    dict_el = w_module.getvalue("dict")
    assert dict_el.getelement(12).value is True
    assert w_module.getvalue("temp").value is True
    assert w_module.getvalue("result").value is False
    assert w_module.getvalue("length").value == 3


def test_interpreter_iterate_dict():
    # dict to list
    ast = parse("""
dict = {'a':5,'b':4,'c':3,'d':2,'e':1,'f':0}
keys = dict get_keys
length = keys len
i = length
list = []
while i:
    key = keys get(length sub(i))
    list add(dict get(key))
    i = i sub(1)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    list_el = [e.value for e in w_module.getvalue("list").elements]
    # all (logical 'and' between list elements)
    # any (logical 'or' between list elements)
    assert all(e in list_el for e in range(5))


def test_interpreter_samekeys_dict():
    ast = parse("""
d = {}
d add(1,2)
d add(1,3)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    d = w_module.getvalue("d")
    assert d.getelement(1).value == 3

ast = parse("""
if 2 mod(3) equals(0):
    a = False
else:
    a = True
""")
interpreter = Interpreter()
w_module = interpreter.make_module()
interpreter.eval(ast, w_module)
print(w_module.getvalue("a").value)
