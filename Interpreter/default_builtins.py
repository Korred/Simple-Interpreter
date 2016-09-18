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

    def equals(x): # ==
        self $int_eq(x)

    def less_than(x): # <
        self $int_less(x)

    def less_equal(x): # <=
        self $int_lesseq(x)

    def greater_than(x): # >
        self $int_greater(x)

    def greater_equal(x): # >=
        self $int_greatereq(x)

object floattrait:
    def add(x):
        self $float_add(x)

    def sub(x):
        self $float_sub(x)

    def mul(x):
        self $float_mul(x)

    def div(x):
        self $float_div(x)

    def equals(x): # ==
        self $float_eq(x)

    def less_than(x): # <
        self $float_less(x)

    def less_equal(x): # <=
        self $float_lesseq(x)

    def greater_than(x): # >
        self $float_greater(x)

    def greater_equal(x): # >=
        self $float_greatereq(x)

object stringtrait:
    def len:
        self $string_length

    def append(x):
        self $string_append(x)

    def reverse:
        self $string_reverse

    def equals(x):
        self $string_equals(x)

object listtrait:
    def add(x):
        self $list_add(x)

    def insert(x,y):
        self $list_insert(x,y)

    def replace(x,y):
        self $list_replace(x,y)

    def del(x):
        self $list_del(x)

    def get(x):
        self $list_get(x)

    def len:
        self $list_len

    def reverse:
        # original list is left untouched
        l = self len
        rev = []
        while l:
            l = l sub(1)
            c = self get(l)
            rev add(c)
        rev

    def oreverse:
        # modifies original list
        x = self reverse
        self clear
        self extend(x)
        self

    def extend(x):
        l = x len
        i = 0
        while l:
            c = x get(i)
            self add(c)
            l = l sub(1)
            i = i add(1)
        self

    def clear:
        self $list_clear


object booltrait:
    def not:
        self $boolean_not

    def and(x):
        self $boolean_and(x)

    def or(x):
        self $boolean_or(x)

    def nand(x):
        self and(x) not

    def nor(x):
        self or(x) not

    def xor(x):
        self $boolean_xor(x)

    def xnor(x):
        self xor(x) not

    def impl(x):
        x or(self not)

    def equals(x):
        self $boolean_equal(x)

object dicttrait:
    def add(x,y):
        self $dict_add(x,y)

    def del(x):
        self $dict_del(x)

    def get(x):
        self $dict_get(x)

    def get_keys(x):
        self $dict_get_keys(x)

    def contains(x):
        self $dict_contains(x)

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

def fibonacci(x):
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
