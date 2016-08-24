# things to change - 

builtin = """
object inttrait:
    def add(x):
        self $int_add(x)

    def sub(x):
        self $int_sub(x)

    def mul(x):
        self $int_mul(x)

    def div(x):
        self $int_div(x)

object floattrait:
    def add(x):
        self $float_add(x)

    def sub(x):
        self $float_sub(x)

    def mul(x):
        self $float_mul(x)

    def div(x):
        self $float_div(x)

object stringtrait:
    def len:
        self $string_length

    def append(x):
        self $string_append(x)

    def reverse:
        self $string_reverse

object listtrait:
    def add(x):
        self $list_add(x)

    def del(x):
        self $list_del(x)

    def get(x):
        self $list_get(x)

    def len:
        self $list_len

    def append(x):
        l = x len
        i = 0
        while l:
            c = x get(i)
            self add(c)
            l = l sub(1)
            i = i add(1)
        self

object dicttrait:
    def add(x,y):
        self $dict_add(x,y)

    def del(x):
        self $dict_del(x)

    def get(x):
        self $dict_get(x)

    def get_keys(x):
        self $dict_get_keys(x)

    def len:
        self $dict_len

def to_int(x):
    $to_int(x)

def to_float(x):
    $to_float(x)

def to_str(x):
    $to_str(x) 

def ceil(x):
    $ceil(x)

def floor(x):
    $floor(x)

# simple range
def s_range(x):
    r = []
    i = 0
    j = x
    while j:
        r add(i)
        i = i add(1)
        j = j sub(1)
    r

# extended range
def e_range(x,y):
    r = []
    s = x
    e = y
    k = e sub(s)
    while k:
        r add(s)
        s = s add(1)
        k = k sub(1)
    r



def fibonacci_iter(x):
    a = 0
    b = 1
    k = x
    while k:
        t = a add(b)
        a = b
        b = t
        k = k sub(1)
    a
"""