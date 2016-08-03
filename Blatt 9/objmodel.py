# prototype-based object model of the language
from c3computation import mro

class W_NormalObject(object):
    # Prototype
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        self.attrs = attrs
        self.parents = []

    def addparent(self, parent_name):
        self.parents.append(parent_name)

    def getc3(self):
        return mro(self)

    def getparents(self):
        return [self.attrs[p] for p in self.parents + ['__parent__'] if p in self.attrs]
        '''
        p = self.getvalue("__parent__")
        if p:
            return [p] + list(self.parents)
        # special case for when self is the outer module - has no parent attr
        else:
            return []
        '''

    def setvalue(self, name, value):
        self.attrs[name] = value

    def getvalue(self, name):
        if (name in self.attrs):
            return self.attrs[name]
        else:
            return None

    def istrue(self):
        return True

    def clone(self):
        # dict(self.attrs) needed to create a copy of self.attrs
        return W_NormalObject(dict(self.attrs))

    def clone(self):
        a = W_NormalObject()
        a.attrs = dict(self.attrs)
        a.parents = list(self.parents)
        return a


class W_Integer(W_NormalObject):
    def __init__(self, value):
        self.value = value
        self.parent = None

    def setvalue(obj, name, value):
        pass  # or raise NotImplementedError()

    def getvalue(self, name):
        return None

    def istrue(self):
        return self.value != 0

    def clone(self):
        return W_Integer(self.value)

    def getparents(self):
        return [self.parent]


class W_Float(W_NormalObject):
    def __init__(self, value):
        self.value = value
        self.parent = None

    def setvalue(obj, name, value):
        pass  # or raise NotImplementedError()

    def getvalue(self, name):
        return None

    def istrue(self):
        return self.value != 0.0

    def clone(self):
        return W_Float(self.value)

    def getparents(self):
        return [self.parent]


class W_Method(W_NormalObject):
    def __init__(self, ast_method):
        self.method = ast_method
        self.attrs = {}
        self.parents = []

    def clone(self):
        a = W_Method(self.method)
        a.attrs = dict(self.attrs)
        a.parents = list(self.parents)
        return a

    def addparent(self, parent):
        self.parents.append(parent)
