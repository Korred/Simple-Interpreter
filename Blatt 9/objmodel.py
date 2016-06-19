# prototype-based object model of the language
'''
There are three types of objects: integers, "normal" objects and methods.
Integers just have an integer value. Normal objects have a set of attributes.
Methods are like normal objects but in addition they also have a reference to an AST node
that the parser produces which describes how the method behaves.

As opposed to the earlier exercises, these classes should not be usable from Python
(so there is no need to override e.g. getattr).
Instead they should have an interface that the interpreter can use.
here are some tests about this in test_objmodel.py.
Write more.
'''

class W_NormalObject(object):
    # Prototype
    def __init__(self, attrs={}):
        self.attrs = attrs

    def setvalue(self, name, value):
        self.attrs[name] = value

    def getvalue(self, name):
        try:
            return self.attrs[name]
        except (KeyError, AttributeError):
            return None

    def istrue(self):
        return True

    def clone(self):
        # dict(self.attrs) needed to create a copy of self.attrs
        return W_NormalObject(dict(self.attrs))


class W_Integer(W_NormalObject):
    def __init__(self, value):
        self.value = value

    def setvalue(obj, name, value):
        pass  # or raise NotImplementedError()

    def istrue(self):
        return self.value != 0

class W_Method(W_NormalObject):
    def __init__(self, ast_method):
        self.method = ast_method
        self.attrs = {}

    def setvalue(obj, name, value):
        pass

    def getvalue(obj, name, value):
        return None
