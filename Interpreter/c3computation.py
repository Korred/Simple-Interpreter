'''
from objmodel import W_NormalObject, W_Method
o = W_NormalObject()
x = W_NormalObject()

y = W_NormalObject()
a = W_NormalObject()
b = W_NormalObject()
c = W_NormalObject()

x.setvalue("__parent__",o)
#x.addparent("__parent__")

y.setvalue("__parent__",o)
#y.addparent("__parent__")

print(x.getparents())
a.addparent(x)
a.addparent(y)
b.addparent(y)

c.addparent(a)
c.addparent(b)
'''


def mro(obj, path=None):
    # path that can be used to check whether circles exist
    if path is None:
        path = [obj]
    elif obj in path:
        raise TypeError("cyclic class hierarchy detected")

    result = [obj]
    parents = obj.getparents()
    sequences = []

    # get mro for all parents
    for p in parents:
        s = mro(p, path)
        sequences.append(s)

    sequences.append(parents)
    while True:
        # check if seq consists of empty lists only
        non_empty = [x for x in sequences if x]
        if not non_empty:
            return result
        for seq in non_empty:
            candidate = seq[0]
            # check wether candidate is valid
            # check all tails [1:] if candidate in tails
            for s in non_empty:
                if candidate in s[1:]:
                    # canidate was found in tail -
                    candidate = None
                    break

            if candidate:
                # candidate found - stop search for now
                break

        if not candidate:
            err = '''no method order resolution found -
             ambiguous hierarchies detected'''
            raise TypeError(err)

        result.append(candidate)
        for seq in sequences:
            try:
                if seq[0] is candidate:
                    del seq[0]
            except IndexError:
                pass
