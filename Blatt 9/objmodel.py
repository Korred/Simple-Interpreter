class W_NormalObject(object):

    def __init__(self,attrs=None):
        if attrs is None:
            attrs = {}
        self.attrs = attrs

    def setvalue(self,name,value):
        self.attrs[name] = value

    def getvalue(self,name):
        if (name in self.attrs):
            return self.attrs[name]
        else:
            return None

    def istrue(self):
        return True

    def clone(self):
        return W_NormalObject(dict(self.attrs))

class W_Integer(W_NormalObject):

    def __init__(self,value):
        self.value = value

    def getvalue(self,name):
        return None

    def istrue(self):
        return self.value != 0

class W_Method(W_NormalObject):

    def __init__(self,ast_method):
        self.method = ast_method
        self.attrs = {}

    def setvalue(self,name,value):
        self.attrs[name] = value

    def getvalue(self,name):
        if (name in self.attrs):
            return self.attrs[name]
        else:
            return None
