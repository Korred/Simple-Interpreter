import operator
from simpleparser import parse
from objmodel import W_Integer, W_Method, W_NormalObject
from objmodel import W_Float, W_List, W_String, W_KeyValue, W_Dict, W_Boolean
import default_builtins
from math import floor, ceil

class Interpreter(object):

    def __init__(self, builtincode=None):
        self.builtin = builtincode

    def eval(self, ast, w_context):
        method = getattr(self, "eval_" + ast.__class__.__name__)
        return method(ast, w_context)

    def eval_Program(self, ast, w_context):
        res = None
        for s in ast.statements:
            res = self.eval(s, w_context)
        return res

    def eval_Assignment(self, ast, w_context):
        # get proper context
        ctx = self.eval(ast.lvalue, w_context)
        # get result
        res = self.eval(ast.expression, ctx)
        ctx.setvalue(ast.attrname, res)

        return res

    def eval_IntLiteral(self, ast, w_context):
        res = W_Integer(ast.value)
        res.parent = add_trait_logic_to_ctx("inttrait", w_context)
        return res

    def eval_FloatLiteral(self, ast, w_context):
        res = W_Float(ast.value)
        res.parent = add_trait_logic_to_ctx("floattrait", w_context)
        return res

    def eval_StringLiteral(self, ast, w_context):
        res = W_String(ast.value)
        res.parent = add_trait_logic_to_ctx("stringtrait", w_context)
        return res


    def eval_BoolLiteral(self, ast, w_context):
        res = W_Boolean(ast.value)
        res.parent = add_trait_logic_to_ctx("booltrait", w_context)
        return res

    def eval_KeyValueLiteral(self, ast, w_context):
        return W_KeyValue(ast.key, ast.value)

    def eval_IfStatement(self, ast, w_context):
        # or if else statement instead of try/except
        try:
            condition = self.eval(ast.condition, w_context).istrue()
        except AttributeError:
            condition = False

        if condition:
            return self.eval(ast.ifblock, w_context)
        elif ast.elseblock:
            return self.eval(ast.elseblock, w_context)

    def eval_MethodCall(self, ast, w_context):
        if ast.receiver.__class__.__name__ == "ImplicitSelf":
            # check mro
            for i in w_context.getc3():
                m = i.getvalue(ast.methodname)
                if m:
                    break

            if m.__class__.__name__ == "W_Method":
                m = m.clone()
                zipped_args = dict(zip(m.attrs["args"], ast.arguments))
                for key in zipped_args:
                    names = ["W_Integer", "W_Float", "W_Method",
                             "W_NormalObject", "W_String", "W_Boolean"]

                    if zipped_args[key].__class__.__name__ not in names:
                        zipped_args[key] = self.eval(zipped_args[key], w_context)
                m.attrs.update(zipped_args)
                res = self.eval(m.method, m)

                return res
            elif m.__class__.__name__ in ("IntLiteral", "FloatLiteral", "StringLiteral", "BoolLiteral"):
                res = self.eval(m, w_context)
                return res
            else:
                return m
        else:
            # different receiver of methodcall
            rec = self.eval(ast.receiver, w_context)
            # eval receiver object
            if rec.__class__.__name__ in ("W_List", "W_Dict", "W_Integer", "W_Float", "W_String", "W_Boolean"):
                for i in w_context.getc3():
                    if (rec.__class__.__name__ == "W_Dict"):
                        ctx = i.getvalue("dicttrait")
                    elif (rec.__class__.__name__ == "W_Integer"):
                        ctx = i.getvalue("inttrait")
                    elif (rec.__class__.__name__ == "W_Float"):
                        ctx = i.getvalue("floattrait")
                    elif (rec.__class__.__name__ == "W_String"):
                        ctx = i.getvalue("stringtrait")
                    elif (rec.__class__.__name__ == "W_Boolean"):
                        ctx = i.getvalue("booltrait")
                    else:
                        ctx = i.getvalue("listtrait")
                    if ctx:
                        break

                # m = method stored in list/dict trait
                m = ctx.getvalue(ast.methodname)

                if ast.arguments:
                    params = []
                    for p in ast.arguments:
                        # eval arguments as receiver later is different
                        # check whether W_Method can be reached here
                        names = ["W_Integer", "W_Float", "W_Method",
                                 "W_NormalObject", "W_String", "W_Boolean"]
                        if p.__class__.__name__ in names:
                            params.append(p)
                        else:
                            res = self.eval(p, w_context)
                            params.append(res)

                # case where m is a W_Method object
                if m.__class__.__name__ == "W_Method":
                    m.setvalue("self", rec)
                    if ast.arguments:
                        zipped_args = dict(zip(m.attrs["args"], params))
                        m.attrs.update(zipped_args)
                    res = self.eval(m.method, m)
                    return res

                elif m.__class__.__name__ in ("W_Integer", "W_Float", "W_String", "W_Boolean"):
                    return m
            # getting receiver from w_context
            # get method by methodname from receiver rec
            for i in rec.getc3():
                m = i.getvalue(ast.methodname)
                if m:
                    break

            m = m.clone()

            if ast.arguments:
                params = []
                for p in ast.arguments:
                    # eval arguments as receiver later is different
                    if p.__class__.__name__ in ["W_NormalObject", "W_Integer", "W_Method", "W_List", "W_Dict" "W_Float", "W_String", "W_Boolean"]:
                        params.append(p)
                    else:
                        res = self.eval(p, w_context)
                        params.append(res)

            # case where m is a W_Method object
            if m.__class__.__name__ == "W_Method":
                m.setvalue("self", rec)
                if ast.arguments:
                    zipped_args = dict(zip(m.attrs["args"], params))
                    m.attrs.update(zipped_args)
                res = self.eval(m.method, m)
                return res

            elif m.__class__.__name__ in ["W_Integer", "W_Float", "W_String", "W_Boolean", "W_List", "W_Dict"]:
                return m

            else:
                pass

    def eval_FunctionDefinition(self, ast, w_context):
        m = W_Method(ast.block)
        m.setvalue("args", ast.arguments)
        # Implicit Parent
        m.setvalue("__parent__", w_context)

        # Additional Parents
        w_context.setvalue(ast.name, m)

    def eval_ExprStatement(self, ast, w_context):
        res = self.eval(ast.expression, w_context)
        return res

    def eval_ObjectDefinition(self, ast, w_context):
        o = W_NormalObject()
        # Implicit Parent
        o.setvalue("__parent__", w_context)
        # set other parents
        if ast.parentnames:
            for i, p in enumerate(ast.parentnames):
                eval_p = self.eval(ast.parentdefinitions[i], w_context)
                o.setvalue(p, eval_p)
                o.addparent(p)

        # set object name
        w_context.setvalue(ast.name, o)
        # set p1 and p2 if provided
        res = self.eval(ast.block, o)
        return res

    def make_module(self):
        # if No bultin provided -> use default builtins
        if self.builtin is None:
            builtin_module = W_NormalObject()
            self.eval(parse(default_builtins.builtin), builtin_module)
            w_module = W_NormalObject()
            w_module.setvalue("__parent__", builtin_module)
            return w_module
        # else use user-provided
        else:
            # create builtin module
            builtin_module = W_NormalObject()
            # parse and eval builtin code
            self.eval(parse(self.builtin), builtin_module)
            # set new module with the builtin module as its parent
            w_module = W_NormalObject()
            w_module.setvalue("__parent__", builtin_module)
            return w_module

    def eval_PrimitiveMethodCall(self, ast, w_context):
        if ast.methodname == "$list_add":
            l = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context)
            l.addelement(param)

        # split from "$list_add" because we need two parameter key and value
        if ast.methodname == "$dict_add":
            l = self.eval(ast.receiver, w_context)
            key = self.eval(ast.arguments[0], w_context)
            value = self.eval(ast.arguments[1], w_context)
            l.addelement(key, value)

        if ast.methodname == "$list_insert":
            l = self.eval(ast.receiver, w_context)
            pos = self.eval(ast.arguments[0], w_context).value
            element = self.eval(ast.arguments[1], w_context)
            l.insert(pos, element)

        if ast.methodname == "$list_replace":
            l = self.eval(ast.receiver, w_context)
            pos = self.eval(ast.arguments[0], w_context).value
            element = self.eval(ast.arguments[1], w_context)
            l.replace(pos, element)

        if ast.methodname == "$dict_get_keys":
            l = self.eval(ast.receiver, w_context)
            return l.getkeys()

        if ast.methodname in ("$list_del", "$dict_del"):
            l = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context).value
            l.delelement(param)

        if ast.methodname in ("$list_len", "$dict_len"):
            l = self.eval(ast.receiver, w_context)
            return W_Integer(l.length)

        if ast.methodname == "$dict_contains":
            s = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context)
            return W_Boolean(s.contains(param))

        if ast.methodname == "$string_length":
            s = self.eval(ast.receiver, w_context)
            return W_Integer(s.length())

        if ast.methodname == "$string_reverse":
            s = self.eval(ast.receiver, w_context)
            return W_String(s.reverse())

        if ast.methodname == "$string_append":
            s = self.eval(ast.receiver, w_context)
            s2 = self.eval(ast.arguments[0], w_context)
            return W_String(s.append(s2))

        if ast.methodname == "$string_equals":
            s = self.eval(ast.receiver, w_context)
            s2 = self.eval(ast.arguments[0], w_context)
            return W_Boolean(s.equals(s2))

        if ast.methodname == "$string_substring":
            s = self.eval(ast.receiver, w_context)
            start = self.eval(ast.arguments[0], w_context)
            end = self.eval(ast.arguments[1], w_context)
            return W_String(s.substring(start,end))

        if ast.methodname in ("$list_get", "$dict_get"):
            l = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context).value
            return l.getelement(param)

        if ast.methodname == "$list_clear":
            l = self.eval(ast.receiver, w_context)
            l.clear()

        if ast.methodname == "$boolean_not":
            b = self.eval(ast.receiver, w_context)
            return W_Boolean(b.simplenot())

        if ast.methodname == "$boolean_and":
            b = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context).value
            return W_Boolean(b.simpleand(param))

        if ast.methodname == "$boolean_or":
            b = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context).value
            return W_Boolean(b.simpleor(param))

        if ast.methodname == "$boolean_xor":
            b = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context).value
            return W_Boolean(b.simplexor(param))

        if ast.methodname == "$boolean_equal":
            b = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context).value
            return W_Boolean(b.equal(param))

        # ceil/floor logic
        if ast.methodname in ("$ceil", "$floor"):
            param = self.eval(ast.arguments[0], w_context)
            val = param.value

            if ast.methodname == "$floor":
                if param.__class__.__name__ == "W_Float":
                    return W_Float(floor(val))
                else:
                    return W_Integer(floor(val))

            if ast.methodname == "$ceil":
                if param.__class__.__name__ == "W_Float":
                    return W_Float(ceil(val))
                else:
                    return W_Integer(ceil(val))

        if ast.methodname in ("$to_int", "$to_float", "$to_str"):
            param = self.eval(ast.arguments[0], w_context)
            val = param.value

            if ast.methodname == "$to_int":
                if param.__class__.__name__ in ("W_Float", "W_Integer"):
                    return W_Integer(int(val))
                if param.__class__.__name__ == "W_String":
                    try:
                        return W_Integer(int(val))
                    except ValueError:
                        raise ValueError('Provided String cannot be parsed to Integer')

            if ast.methodname == "$to_float":
                if param.__class__.__name__ in ("W_Float", "W_Integer"):
                    return W_Float(float(val))
                if param.__class__.__name__ == "W_String":
                    try:
                        return W_Float(float(val))
                    except ValueError:
                        raise ValueError('Provided String cannot be parsed to Float')

            if ast.methodname == "$to_str":
                if param.__class__.__name__ in ("W_Float", "W_Integer", "W_String"):
                    try:
                        return W_String(str(val))
                    except ValueError:
                        raise ValueError('Provided Type cannot be parsed to String')

        # numeric operations
        num_op = ['$int_add',
                  '$int_sub',
                  '$int_mul',
                  '$int_div',
                  '$float_add',
                  '$float_sub',
                  '$float_mul',
                  '$float_div']

        # comparision 
        comp_op = ['$int_eq',
                   '$int_less',
                   '$int_lesseq',
                   '$int_greater',
                   '$int_greatereq',
                   '$float_eq',
                   '$float_less',
                   '$float_lesseq',
                   '$float_greater',
                   '$float_greatereq']

        if ast.methodname in num_op:
            # Flags necessary to decide whether to return a float or an int
            l = self.eval(ast.receiver, w_context)
            l_flag = False
            r_flag = False
            if l.__class__.__name__ == "W_Float":
                l_flag = True
            l = l.value

            # add/sub/mul/div logic
            if ast.methodname in ("$int_add", "$float_add"):
                op = operator.add
            elif ast.methodname in ("$int_sub", "$float_sub"):
                op = operator.sub
            elif ast.methodname in ("$int_mul", "$float_mul"):
                op = operator.mul
            elif ast.methodname in ("$int_div", "$float_div"):
                op = operator.truediv

            for e in ast.arguments:
                r = self.eval(e, w_context)
                if r.__class__.__name__ == "W_Float":
                    r_flag = True

                r = r.value
                l = op(l, r)

            if l_flag or r_flag:
                return W_Float(l)
            else:
                return W_Integer(int(l))

        if ast.methodname in comp_op:
            l = self.eval(ast.receiver, w_context)
            r = self.eval(ast.arguments[0], w_context)

            l_class = l.__class__.__name__
            r_class = r.__class__.__name__
            valid = ["W_Float", "W_Integer"]

            if l_class in valid and r_class in valid:
                if "_eq" in ast.methodname:
                    op = operator.eq
                elif "_lesseq" in ast.methodname:
                    op = operator.le
                elif "_less" in ast.methodname:
                    op = operator.lt
                elif "_greatereq" in ast.methodname:
                    op = operator.ge
                elif "_greater" in ast.methodname:
                    op = operator.gt

                comp = op(l.value, r.value)
                return W_Boolean(comp)
            else:
                raise TypeError("Cannot compare {} and {}".format(
                    l_class, r_class))

    def eval_WhileStatement(self, ast, w_context):
        res = None
        if not self.eval(ast.condition, w_context).istrue():
            pass
        else:
            while self.eval(ast.condition, w_context).istrue():
                res = self.eval(ast.whileblock, w_context)
        return res

    def eval_ImplicitSelf(self, ast, w_context):
        return w_context

    def eval_ListLiteral(self, ast, w_context):
        res = []
        for e in ast.elements:
            part = self.eval(e, w_context)
            res.append(part)
        res = W_List(res)
        res.parent = add_trait_logic_to_ctx("listtrait", w_context)

        return res

    def eval_DictLiteral(self, ast, w_context):
        res = []
        for e in ast.elements:
            part = self.eval(e, w_context)
            res.append(part)
        res = W_Dict(res)
        res.parent = add_trait_logic_to_ctx("dicttrait", w_context)

        return res

def add_trait_logic_to_ctx(trait, w_context):
    for i in w_context.getc3():
        ctx = i.getvalue(trait)
        if ctx:
            break
    return ctx
