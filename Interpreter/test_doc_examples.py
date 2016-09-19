from simpleparser import parse
from interpreter import Interpreter
from simpleast import *

# Additional tests for (built-in) examples mentioned in the documentation


def test_doc_int_float():
    ast = parse("""
sum1 = 5 add(5)
sum2 = 5.0 add(5.0)
sum3 = 5.0 add(5)

dif1 = 5 sub(5)
dif2 = 5.0 sub(5.0)
dif3 = 5.0 sub(5)

prod1 = 5 mul(5)
prod2 = 5.0 mul(5.0)
prod3 = 5.0 mul(5)

quot1 = 5 div(2)
quot2 = 5.0 div(2.0)
quot3 = 5.0 div(2)

""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert isinstance(w_module.getvalue("sum1").value, int)
    assert w_module.getvalue("sum1").value == 10
    assert isinstance(w_module.getvalue("sum2").value, float)
    assert w_module.getvalue("sum2").value == 10.0
    assert isinstance(w_module.getvalue("sum3").value, float)
    assert w_module.getvalue("sum3").value == 10.0

    assert isinstance(w_module.getvalue("dif1").value, int)
    assert w_module.getvalue("dif1").value == 0
    assert isinstance(w_module.getvalue("dif2").value, float)
    assert w_module.getvalue("dif2").value == 0.0
    assert isinstance(w_module.getvalue("dif3").value, float)
    assert w_module.getvalue("dif3").value == 0.0

    assert isinstance(w_module.getvalue("prod1").value, int)
    assert w_module.getvalue("prod1").value == 25
    assert isinstance(w_module.getvalue("prod2").value, float)
    assert w_module.getvalue("prod2").value == 25.0
    assert isinstance(w_module.getvalue("prod3").value, float)
    assert w_module.getvalue("prod3").value == 25.0

    assert isinstance(w_module.getvalue("quot1").value, int)
    assert w_module.getvalue("quot1").value == 2
    assert isinstance(w_module.getvalue("quot2").value, float)
    assert w_module.getvalue("quot2").value == 2.5
    assert isinstance(w_module.getvalue("quot3").value, float)
    assert w_module.getvalue("quot3").value == 2.5


def test_doc_string():
    ast = parse("""
str1 = '01234'
str2 = '56789'
str3 = '9876543210'

length = str1 len
appended = str1 append(str2)
reversed = appended reverse
eq = reversed equals(str3)
n_eq = appended equals(str3)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("length").value == 5
    assert w_module.getvalue("appended").value == '0123456789'
    assert w_module.getvalue("reversed").value == '9876543210'
    assert w_module.getvalue("eq").value is True
    assert w_module.getvalue("n_eq").value is False


def test_doc_boolean():
    ast = parse("""
b1 = True not
b2 = True and(False)
b3 = True or(False)
b4 = True nand(False)
b5 = True nor(False)
b6 = True xor(True)
b7 = True xnor(False)
b8 = True impl(True)
b9 = True equals(True)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)
    assert w_module.getvalue("b1").value is False
    assert w_module.getvalue("b2").value is False
    assert w_module.getvalue("b3").value is True
    assert w_module.getvalue("b4").value is True
    assert w_module.getvalue("b5").value is False
    assert w_module.getvalue("b6").value is False
    assert w_module.getvalue("b7").value is False
    assert w_module.getvalue("b8").value is True
    assert w_module.getvalue("b9").value is True


def test_doc_list():
    ast = parse("""
l1 = [1,2,3]
l1 add(4)

l2 = [1,3]
l2 insert(1,2)

l3 = [1,3]
l3 replace(1,2)

l4 = [1]
l4 del(0)

l5 = [1,2,3] get(0)

length = [1,2,3] len

r1 = [1,2,3] reverse

l6 = [1,2,3]
r2 = l6 oreverse

l7 = [1,2,3] extend([4,5,6])

l8 = [1,2,3]
l8 clear


""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    l1 = w_module.getvalue("l1").elements
    l2 = w_module.getvalue("l2").elements
    l3 = w_module.getvalue("l3").elements
    l4 = w_module.getvalue("l4").elements
    l5 = w_module.getvalue("l5").value
    length = w_module.getvalue("length").value
    r1 = w_module.getvalue("r1").elements
    l6 = w_module.getvalue("l6").elements
    l7 = w_module.getvalue("l7").elements
    l8 = w_module.getvalue("l8").elements

    assert [l.value for l in l1] == [1, 2, 3, 4]
    assert [l.value for l in l2] == [1, 2, 3]
    assert [l.value for l in l3] == [1, 2]
    assert [l.value for l in l4] == []
    assert l5 == 1
    assert length == 3
    assert [l.value for l in r1] == [3, 2, 1]
    assert [l.value for l in l6] == [3, 2, 1]
    assert [l.value for l in l7] == [1, 2, 3, 4, 5, 6]
    assert [l.value for l in l8] == []


def test_doc_mixed():
    ast = parse("""
i = to_int(2.5)
f = to_float("2.5")
s = to_str(1.337)

ce = ceil(2.6)
fl = floor(2.6)

l1 = s_range(5)
l2 = e_range(5,10)

pos # 0 1 2 3 4 5 6 7  8
ele # 0 1 1 2 3 5 8 13 21
fib = fibonacci(8)
""")
    interpreter = Interpreter()
    w_module = interpreter.make_module()
    interpreter.eval(ast, w_module)

    assert isinstance(w_module.getvalue("i").value, int)
    assert w_module.getvalue("i").value == 2

    assert isinstance(w_module.getvalue("f").value, float)
    assert w_module.getvalue("f").value == 2.5

    assert isinstance(w_module.getvalue("s").value, str)
    assert w_module.getvalue("s").value == "1.337"

    assert w_module.getvalue("ce").value == 3
    assert w_module.getvalue("fl").value == 2

    l1 = w_module.getvalue("l1").elements
    assert [i.value for i in l1] == [0, 1, 2, 3, 4]

    l2 = w_module.getvalue("l2").elements
    assert [i.value for i in l2] == [5, 6, 7, 8, 9]

    assert w_module.getvalue("fib").value == 21
