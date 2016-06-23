# prototype-based object model of the language

class W_NormalObject(object):
    # Prototype
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        self.attrs = attrs


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


class W_Integer(W_NormalObject):
    def __init__(self, value):
        self.value = value

    def setvalue(obj, name, value):
        pass  # or raise NotImplementedError()

    def getvalue(self,name):
        return None

    def istrue(self):
        return self.value != 0

    def clone(self):
        return W_Integer(self.value)

class W_Method(W_NormalObject):
    def __init__(self, ast_method):
        self.method = ast_method
        self.attrs = {}

    def clone(self):
        a = W_Method(self.method)
        a.attrs = dict(self.attrs)
        return a
