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
        return [self.attrs[p] for p in self.parents + ['__parent__']
                if p in self.attrs]

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
        a = W_NormalObject()
        a.attrs = dict(self.attrs)
        a.parents = list(self.parents)
        return a


class W_Integer(W_NormalObject):
    def __init__(self, value):
        self.value = int(value)
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


class W_Boolean(W_NormalObject):
    def __init__(self, value):
        self.value = value
        self.parent = None

    def setvalue(obj, name, value):
        pass

    def getvalue(self, name):
        return None

    def istrue(self):
        return self.value

    def simplenot(self):
        return not(self.value)

    def simpleand(self, param):
        if self.value and param:
            return True
        else:
            return False

    def simpleor(self, param):
        if self.value or param:
            return True
        else:
            return False

    def simplexor(self, param):
        if ((self.value and not(param)) or
           (not(self.value) & param)):
            return True
        else:
            return False

    def clone(self):
        return W_Boolean(self.value)

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


class W_String(W_NormalObject):
    def __init__(self, value):
        self.value = value
        self.parent = None

    def setvalue(obj, name, value):
        pass

    def getvalue(self, name):
        return None

    def append(self, string):
        return self.value + string.value

    def length(self):
        return len(self.value)

    def reverse(self):
        return self.value[::-1]

    def equals(self, string):
        if (self.value == string.value):
            return True
        else:
            return False

    def istrue(self):
        return self.value != ""

    def clone(self):
        return W_String(self.value)

    def getparents(self):
        return [self.parent]


class W_KeyValue(W_NormalObject):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None

    def setvalue(obj, name, value):
        pass

    def getvalue(self, name):
        return None

    def istrue(self):
        return (self.key is not None) & (self.value is not None)

    def clone(self):
        return W_KeyValue(self.key, self.value)

    def getparents(self):
        return [self.parent]


class W_List(W_NormalObject):
    def __init__(self, elements):
        if elements is None:
            elements = []
        self.elements = elements
        self.parent = None
        self.length = len(elements)

    def getelement(self, index):
        try:
            element = self.elements[index]
            return element
        except IndexError:
            raise IndexError("Provided Index does not exist!")

    def addelement(self, element):
        self.elements.append(element)
        self.length += 1

    def insert(self, pos, element):
        self.elements.insert(pos, element)

    def replace(self, pos, element):
        try:
            self.elements[pos] = element
        except IndexError:
            self.addelement(element)

    def istrue(self):
        return self.length != 0

    def delelement(self, index):
        try:
            self.elements.pop(index)
            self.length -= 1
        except IndexError:
            raise IndexError("Provided Index does not exist!")

    def clear(self):
        self.elements = []

    def clone(self):
        return W_List(self.elements)

    def getparents(self):
        return [self.parent]


class W_Dict(W_NormalObject):
    def __init__(self, elements):
        if elements is None:
            elements = []
        self.elements = {}
        for kv in elements:
            key = kv.key.value
            self.elements[key] = kv.value
        self.parent = None
        self.length = len(elements)

    def getelement(self, key):
        try:
            element = self.elements.get(key)
            return element
        except IndexError:
            raise IndexError("Provided Index does not exist!")

    def addelement(self, key, value):
        self.elements[key.value] = value
        self.length += 1

    # return the keys to be able to iterate over a dictionary
    def getkeys(self):
        elements = []
        for k in list(self.elements.keys()):
            if (isinstance(k, str)):
                elements.append(W_String(k))
            elif (isinstance(k, float)):
                elements.append(W_Float(k))
            else:
                elements.append(W_Integer(k))
        return W_List(elements)

    def contains(self, key):
        keyobjects = self.getkeys().elements
        keys = [k.value for k in keyobjects]
        return (key.value in keys)

    def istrue(self):
        return self.length != 0

    def delelement(self, key):
        try:
            del self.elements[key]
            self.length -= 1
        except KeyError:
            # nothing to do, don't raise a key error
            pass

    def clone(self):
        return W_Dict(self.elements)

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
