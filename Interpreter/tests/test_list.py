import sys
sys.path.append("..")
from simpleparser import parse
from simplelexer import lex
from interpreter import Interpreter
from simpleast import *

# Lexer Tests


def test_lex_list_int():
    s = "[1,2,3,4,5,6]"
    tokens = lex(s)
    x = ["ListOpenBracket", "Number", "Comma",
         "Number", "Comma", "Number", "Comma",
         "Number", "Comma", "Number", "Comma",
         "Number", "ListCloseBracket", "Newline",
         "EOF"]
    for i, t in enumerate(tokens):
        assert t.name == x[i]


def test_lex_list_float():
    s = "[1.0,-2.0,3.123,0.0000,-5.125,-0.000]"
    tokens = lex(s)
    x = ["ListOpenBracket", "Float", "Comma",
         "Float", "Comma", "Float", "Comma",
         "Float", "Comma", "Float", "Comma",
         "Float", "ListCloseBracket", "Newline",
         "EOF"]
    for i, t in enumerate(tokens):
        assert t.name == x[i]


def test_lex_list_string():
    s = """["a","v","z",'i','j','choochoo']"""
    tokens = lex(s)
    x = ["ListOpenBracket", "String", "Comma",
         "String", "Comma", "String", "Comma",
         "String", "Comma", "String", "Comma",
         "String", "ListCloseBracket", "Newline",
         "EOF"]
    for i, t in enumerate(tokens):
        assert t.name == x[i]


def test_lex_list_mixed():
    s = """[1,2,3.0,-4.2,'2',"abc"]"""
    tokens = lex(s)
    x = ["ListOpenBracket", "Number", "Comma",
         "Number", "Comma", "Float", "Comma",
         "Float", "Comma", "String", "Comma",
         "String", "ListCloseBracket", "Newline",
         "EOF"]
    for i, t in enumerate(tokens):
        assert t.name == x[i]


def test_lex_list_in_list():
    s = """[[1,2,3],[4,5,6]]"""
    tokens = lex(s)
    x = ["ListOpenBracket", "ListOpenBracket", "Number",
         "Comma", "Number", "Comma", "Number", "ListCloseBracket",
         "Comma", "ListOpenBracket", "Number", "Comma", "Number",
         "Comma", "Number", "ListCloseBracket", "ListCloseBracket",
         "Newline", "EOF"]
    for i, t in enumerate(tokens):
        assert t.name == x[i]

# Parser Tests


def test_list_simple_expression():
    ast = parse("[1,2]")
    res = Program([ExprStatement(ListLiteral([IntLiteral(1), IntLiteral(2)]))])

    assert ast == res


def test_list_simple_assignment():
    ast = parse("a = [1,2]")
    res = Program([Assignment(
        ImplicitSelf(),
        'a',
        ListLiteral([IntLiteral(1), IntLiteral(2)]))])

    assert ast == res


def test_list_simple_primitive():
    ast = parse("[1] $add(2)")
    res = Program([ExprStatement(PrimitiveMethodCall(
        ListLiteral([IntLiteral(1)]), '$add', [IntLiteral(2)]))])

    assert ast == res


def test_list_empty():
    ast = parse("[]")
    res = Program([ExprStatement(ListLiteral([]))])

    assert ast == res


# Interpreter Tests

def test_list_i_simple():
    ast = parse("""
a = [1,2,3,4]
b = [-1.555,0.0,+1.5,5]
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    for i in range(4):
        assert w_module.getvalue("a").elements[i].value == i + 1

    assert isinstance(w_module.getvalue("b").elements[0].value, float)
    assert isinstance(w_module.getvalue("b").elements[1].value, float)
    assert isinstance(w_module.getvalue("b").elements[2].value, float)
    assert isinstance(w_module.getvalue("b").elements[3].value, int)

    assert w_module.getvalue("b").elements[0].value == -1.555
    assert w_module.getvalue("b").elements[1].value == 0.0
    assert w_module.getvalue("b").elements[2].value == +1.5
    assert w_module.getvalue("b").elements[3].value == 5


def test_list_length():
    ast = parse("""
a = [1,2,3,4]
a del(1)
l1 = a len
a add(5)
a add(6)
l2 = a len
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("l1").value == 3
    assert w_module.getvalue("l2").value == 5
    res = [1, 3, 4, 5, 6]
    assert [a.value for a in w_module.getvalue("a").elements] == res


def test_list_i_def():
    ast = parse("""
def o:
    # function that simply returns a list
    [1,2,3,4]
a = o
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    res = list(range(1, 5))
    assert [a.value for a in w_module.getvalue("a").elements] == res


def test_list_i_inlist():
    ast = parse("""
a = [[1,2,3,4],[5,6,7,8]]
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    a1 = [1, 2, 3, 4]
    a2 = [5, 6, 7, 8]
    assert [e.value for e in w_module.getvalue("a").elements[0].elements] == a1
    assert [e.value for e in w_module.getvalue("a").elements[1].elements] == a2


def test_list_i_add():
    ast = parse("""
a = []
# add int to list
a add(1)

# add list to list
a add([1])
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").elements[0].value == 1
    assert w_module.getvalue("a").elements[1].elements[0].value == 1


def test_list_i_del():
    ast = parse("""
a = [1,2,3]
b = [1,2,3]
c = [1,2,3]
a del(0) #first
b del(1) #middle
c del(2) #last
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert [e.value for e in w_module.getvalue("a").elements] == [2, 3]
    assert [e.value for e in w_module.getvalue("b").elements] == [1, 3]
    assert [e.value for e in w_module.getvalue("c").elements] == [1, 2]


def test_list_i_del_error():
    ast = parse("""
a = [1,2,3]
a del(6)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    py.test.raises(IndexError, interpreter.eval, ast, w_module)


def test_clear_list():
    ast = parse("""
a = [1,2,3,4,5]
a clear
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("a").elements == []


def test_list_i_extend():
    ast = parse("""
a = [1,2]
b = [3,4]
c = a extend(b)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    res = list(range(1, 5))
    assert [a.value for a in w_module.getvalue("c").elements] == res


def test_list_i_range():
    ast = parse("""
s = s_range(5)
e = e_range(5,10)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    for i in range(5):
        assert w_module.getvalue("s").elements[i].value == i
    for i in range(5, 10):
        assert w_module.getvalue("e").elements[i - 5].value == i


def test_list_i_fibonacci():
    ast = parse("""
f = fibonacci(6)

def fib_list(x):
    r = []
    i = 0
    k = x add(1)

    while k:
        f = fibonacci(i)
        r add(f)
        i = i add(1)
        k = k sub(1)
    r

l = fib_list(6)

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert w_module.getvalue("f").value == 8
    t = [0, 1, 1, 2, 3, 5, 8]
    assert [e.value for e in w_module.getvalue("l").elements] == t


def test_simple_rev_list():
    ast = parse("""
a = [1,2,3,4,5]
rev = a reverse
orev = a oreverse
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    t = [5, 4, 3, 2, 1]
    assert [e.value for e in w_module.getvalue("rev").elements] == t
    assert [e.value for e in w_module.getvalue("orev").elements] == t
    assert [e.value for e in w_module.getvalue("a").elements] == t


def test_mixed_rev_list():
    ast = parse("""
a = [1,"a",1.2,[1,2],{1:2}]
rev = a reverse
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    l = w_module.getvalue("rev").elements
    assert l[4].value == 1
    assert l[3].value == "a"
    assert l[2].value == 1.2
    assert [a.value for a in l[1].elements] == [1, 2]
    assert l[0].getelement(1).value == 2


def test_variable_list():
    ast = parse("""
a = 1
b = 2
c = [3,4,5]
d = [a,b,c]
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    x = w_module.getvalue("d").elements
    assert x[0].value == 1
    assert x[1].value == 2
    assert [a.value for a in x[2].elements] == [3, 4, 5]


def test_list_insert():
    ast = parse("""
a = [1,2,3]
a insert(0,0)
a insert(4,4)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    x = w_module.getvalue("a").elements
    assert [a.value for a in x] == [0, 1, 2, 3, 4]


def test_list_get():
    ast = parse("""
a = [1,2,3]
b = a get(0)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("b").value == 1


def test_list_replace():
    ast = parse("""
a = [1,2,3]
a replace(0,0)
a replace(6,"test")

b = [[1,2,3]]
rep1 = b get(0)
rep1 replace(2,1337)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    x1 = w_module.getvalue("a").elements
    assert [a.value for a in x1] == [0, 2, 3, "test"]

    x2 = w_module.getvalue("rep1").elements
    assert [a.value for a in x2] == [1, 2, 1337]
