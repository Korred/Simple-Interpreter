import py
import operator
from simpleparser import parse
from objmodel import W_Integer, W_Method, W_NormalObject, W_Float, W_List
import default_builtins
import pdb
from math import floor, ceil


class Interpreter(object):

    def __init__(self,builtincode=None):
        self.builtin = builtincode

    def eval(self, ast, w_context):
        method = getattr(self, "eval_" + ast.__class__.__name__)
        return method(ast, w_context)

    def eval_Program(self, ast, w_context):
        print()
        print("### Evaluating program ###")
        print(ast)
        res = None
        for s in ast.statements:
            res = self.eval(s, w_context)
        return res

    def eval_Assignment(self, ast, w_context):
        print()
        print("### Evaluating assignment ###")
        print(ast.lvalue)
        # get proper context
        ctx = self.eval(ast.lvalue, w_context)
        # get result
        res = self.eval(ast.expression, ctx)
        ctx.setvalue(ast.attrname, res)

        print("ASSIGN", ast.attrname, res)
        return res

    def eval_IntLiteral(self, ast, w_context):
        print()
        print("### Evaluating IntLiteral ###")
        print(W_Integer(ast.value).value)
        print(ast)
        res = W_Integer(ast.value)
        for i in w_context.getc3():
            ctx = i.getvalue("inttrait")
            if ctx:
                break
        res.parent = ctx

        return res

    def eval_FloatLiteral(self, ast, w_context):
        print()
        print("### Evaluating FloatLiteral ###")
        print(W_Float(ast.value).value)
        res = W_Float(ast.value)
        for i in w_context.getc3():
            ctx = i.getvalue("floattrait")
            if ctx:
                break
        res.parent = ctx

        return res

    def eval_IfStatement(self, ast, w_context):
        # or if else statement instead of try/except
        print()
        print("### Evaluating IFStatement ###")
        print(ast)
        try:
            condition = self.eval(ast.condition, w_context).istrue()
        except AttributeError:
            condition = False
        print(condition)

        if condition:
            return self.eval(ast.ifblock, w_context)
        elif ast.elseblock:
            return self.eval(ast.elseblock, w_context)

    def eval_MethodCall(self, ast, w_context):
        print()
        print("### Evaluating MethodCall ###")
        print("AST: ", ast)
        if ast.receiver.__class__.__name__ == "ImplicitSelf":
            print("RECEIVER = IMPLICITSELF")
            print("ATTRIBUTES: ", w_context.attrs)
            # get lookup order (C3 MRO)

            print("METHODNAME: ", ast.methodname)
            print("CONTEXT: ", w_context)
            print("PARENTS: ", w_context.getparents())
            print("MRO LIST ", w_context.getc3())

            print("CHECKING MRO")
            for i in w_context.getc3():
                m = i.getvalue(ast.methodname)
                i_name = i
                if m:
                    break

            print("FOUND:", m.__class__.__name__, "in",i)
            if m.__class__.__name__ == "W_Method":
                m = m.clone()
                print("METHOD ATTRS: ", m.attrs)
                zipped_args = dict(zip(m.attrs["args"],ast.arguments))
                for key in zipped_args:
                    if zipped_args[key].__class__.__name__ not in ["W_Integer", "W_Float", "W_Method", "W_NormalObject"]:
                        zipped_args[key] = self.eval(zipped_args[key], w_context)
                m.attrs.update(zipped_args)
                print(m.attrs)
                res = self.eval(m.method, m)
                print(res)

                return res
            elif m.__class__.__name__ == "IntLiteral":
                res = self.eval(m, w_context)
                return res
            elif m.__class__.__name__ == "W_Integer":
                print(m.value)
                return m
            elif m.__class__.__name__ == "FloatLiteral":
                res = self.eval(m, w_context)
                return res
            elif m.__class__.__name__ == "W_Float":
                print(m.value)
                return m
            elif m.__class__.__name__ == "W_NormalObject":
                return m

            elif m.__class__.__name__ == "W_List":
                print(m.elements)
                return m
        else:
            # different receiver of methodcall
            print("REC:", ast.receiver.__class__.__name__)
            rec = self.eval(ast.receiver, w_context)
            # eval reciever object



            # inttrait logic
            if rec.__class__.__name__ == "W_Integer":
                print("REC:", ast.receiver)
                print("METHODNAME:", ast.methodname)
                print("CHECKING MRO")
                for i in w_context.getc3():
                    ctx = i.getvalue("inttrait")
                    if ctx:
                        break
                print("INTTRAIT:", ctx)
                # "object found"
                m = ctx.getvalue(ast.methodname)

                if ast.arguments:
                    print("ARGUMENTS FOUND")
                    params = []
                    for p in ast.arguments:
                        # eval arguments as receiver later is different
                        print(p.__class__.__name__)
                        if p.__class__.__name__ in ["W_NormalObject", "W_Integer", "W_Float", "W_Method"]:
                            params.append(p)
                        else:
                            # it might be necessary to handle different edge cases here
                            # or maybe not... should be tested accordingly
                            res = self.eval(p, w_context)
                            params.append(res)
                    print("params", params)

                # case where is a W_Method object
                if m.__class__.__name__ == "W_Method":
                    m.setvalue("self", rec)
                    if ast.arguments:
                        zipped_args = dict(zip(m.attrs["args"], params))
                        m.attrs.update(zipped_args)
                        print("X", m.attrs)
                    res = self.eval(m.method, m)
                    return res

                elif m.__class__.__name__ == "W_Integer":
                    print(m, m.value)
                    return m

            # floattrait logic
            if rec.__class__.__name__ == "W_Float":
                print("REC:", ast.receiver)
                print("METHODNAME:", ast.methodname)
                print("CHECKING MRO")
                for i in w_context.getc3():
                    ctx = i.getvalue("floattrait")
                    if ctx:
                        break
                print("FLOATTRAIT:", ctx)
                # "object found"
                m = ctx.getvalue(ast.methodname)

                if ast.arguments:
                    print("ARGUMENTS FOUND")
                    params = []
                    for p in ast.arguments:
                        # eval arguments as receiver later is different
                        print(p.__class__.__name__)
                        if p.__class__.__name__ in ["W_NormalObject", "W_Integer", "W_Float", "W_Method"]:
                            params.append(p)
                        else:
                            # it might be necessary to handle different edge cases here
                            # or maybe not... should be tested accordingly
                            res = self.eval(p, w_context)
                            params.append(res)
                    print("params", params)

                # case where m is a W_Method object
                if m.__class__.__name__ == "W_Method":
                    m.setvalue("self", rec)
                    if ast.arguments:
                        zipped_args = dict(zip(m.attrs["args"], params))
                        m.attrs.update(zipped_args)
                        print("X", m.attrs)
                    res = self.eval(m.method, m)
                    return res

                elif m.__class__.__name__ == "W_Integer":
                    print(m,m.value)
                    return m

                elif m.__class__.__name__ == "W_Float":
                    print(m,m.value)
                    return m



            if rec.__class__.__name__ == "W_List":
                print("REC:", ast.receiver)
                print("METHODNAME:", ast.methodname)
                print("CHECKING MRO")
                for i in w_context.getc3():
                    ctx = i.getvalue("listtrait")
                    if ctx:
                        break
                print("LISTTRAIT:", ctx)

                # m = method stored in listtrait
                m = ctx.getvalue(ast.methodname)
                print(m)

                if ast.arguments:
                    print("ARGUMENTS FOUND")
                    params = []
                    for p in ast.arguments:
                        # eval arguments as receiver later is different
                        print(p.__class__.__name__)
                        # check whether W_Method can be reached here
                        # should include strings maybe
                        if p.__class__.__name__ in ["W_NormalObject", "W_Integer", "W_Float", "W_Method"]:
                            params.append(p)
                        else:
                            # it might be necessary to handle different edge cases here
                            # or maybe not... should be tested accordingly
                            res = self.eval(p, w_context)
                            params.append(res)
                    print("params", params)


                # case where m is a W_Method object
                if m.__class__.__name__ == "W_Method":
                    m.setvalue("self", rec)
                    if ast.arguments:
                        zipped_args = dict(zip(m.attrs["args"], params))
                        m.attrs.update(zipped_args)
                        print("X", m.attrs)
                    res = self.eval(m.method, m)
                    return res

                elif m.__class__.__name__ == "W_Integer":
                    print(m,m.value)
                    return m

                elif m.__class__.__name__ == "W_Float":
                    print(m,m.value)
                    return m














            print("RECEIVER =",ast.receiver.methodname)
            # getting receiver from w_context
            
            print(2,rec.__class__.__name__)
            print(3,rec.attrs)

            # get method by methodname from receiver rec
            print("CHECKING MRO")
            for i in rec.getc3():
                m = i.getvalue(ast.methodname)
                if m:
                    break

            print("FOUND: ", m.__class__.__name__)
            m = m.clone()

            print("ARGUMENTS: ",ast.arguments)

            if ast.arguments:
                print("ARGUMENTS FOUND")
                params = []
                for p in ast.arguments:
                    # eval arguments as receiver later is different
                    print(p.__class__.__name__)
                    if p.__class__.__name__ in ["W_NormalObject", "W_Integer", "W_Method"]:
                        params.append(p)
                    else:
                        # it might be necessary to handle different edge cases here
                        # or maybe not... should be tested accordingly
                        res = self.eval(p, w_context)
                        params.append(res)
                print("params", params)

            # case where is a W_Method object
            if m.__class__.__name__ == "W_Method":
                m.setvalue("self", rec)
                if ast.arguments:
                    zipped_args = dict(zip(m.attrs["args"], params))
                    m.attrs.update(zipped_args)
                    print("X", m.attrs)
                res = self.eval(m.method, m)
                return res

            elif m.__class__.__name__ == "W_Integer":
                print(m)
                return m

            else:
                print("WHAT AN ELSE CASE HERE??")
                pass

    def eval_FunctionDefinition(self, ast, w_context):
        print()
        print("### Evaluating FunctionDef ###")
        print("AST: ", ast)
        print("BLOCK: ",ast.block)
        m = W_Method(ast.block)
        print("method:",m)
        m.setvalue("args", ast.arguments)
        # Implicit Parent
        m.setvalue("__parent__", w_context)

        # Additional Parents
        print(m.attrs)
        w_context.setvalue(ast.name, m)

    def eval_ExprStatement(self, ast, w_context):
        print()
        print("### Evaluating ExprStatement ###")
        print(1, ast)
        print(2, w_context.attrs)
        res = self.eval(ast.expression, w_context)
        return res

    def eval_ObjectDefinition(self, ast, w_context):
        print()
        print("### Evaluating ObjectDefinition ###")
        print(ast)
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
        # if No bultin provided -> use default buildins
        if self.builtin is None:
            builtin_module = W_NormalObject()
            self.eval(parse(default_builtins.builtin),builtin_module)
            w_module = W_NormalObject()
            w_module.setvalue("__parent__", builtin_module)
            return w_module
        # else use user-provided
        else:
            # create builtin module
            builtin_module = W_NormalObject()
            # parse and eval builtin code
            self.eval(parse(self.builtin),builtin_module)
            # new module with the builtin module as its parent
            w_module = W_NormalObject()
            w_module.setvalue("__parent__", builtin_module)
            return w_module

    def eval_PrimitiveMethodCall(self, ast, w_context):
        print()
        print("### Evaluating PrimitiveMethodCall ###")

        if ast.methodname == "$list_add":
            print("AST:", ast)
            l = self.eval(ast.receiver, w_context)
            print(l)
            print(ast.arguments[0])
            param = self.eval(ast.arguments[0], w_context)
            l.addelement(param)

        if ast.methodname == "$list_del":
            print("AST:", ast)
            l = self.eval(ast.receiver, w_context)
            print(l)
            print(ast.arguments[0])
            param = self.eval(ast.arguments[0], w_context).value
            l.delelement(param)

        if ast.methodname == "$list_len":
            l = self.eval(ast.receiver, w_context)
            return W_Integer(l.length)

        if ast.methodname == "$list_get":
            l = self.eval(ast.receiver, w_context)
            param = self.eval(ast.arguments[0], w_context).value
            return l.getelement(param)




        # ceil/floor logic
        if ast.methodname in ("$ceil", "$floor"):
            print("AST:", ast)
            print(ast.arguments[0])
            param = self.eval(ast.arguments[0], w_context)
            print(param)
            val = param.value
            if ast.methodname == "$floor":
                if param.__class__.__name__ == "W_Float":
                    return W_Float(float(floor(val)))
                else:
                    return W_Integer(floor(val))
            if ast.methodname == "$ceil":
                if param.__class__.__name__ == "W_Float":
                    return W_Float(float(ceil(val)))
                else:
                    return W_Integer(ceil(val))


        if "int" in ast.methodname or "float" in ast.methodname:
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

            
            # Flags necessary to decide whether to return a float or an int


            for e in ast.arguments:
                r = self.eval(e, w_context)
                if r.__class__.__name__ == "W_Float":
                    r_flag = True

                r = r.value
                l = op(l, r)

            if l_flag or r_flag:
                print (l)
                return W_Float(l)
            else:
                return W_Integer(int(l))

    def eval_WhileStatement(self, ast, w_context):
        print("EVAL WHILE")
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
        print("\n### Evaluating ListLiteral ###")
        print(ast.elements)
        res = []
        for e in ast.elements:
            part = self.eval(e, w_context)
            res.append(part)
        res = W_List(res)

        for i in w_context.getc3():
            ctx = i.getvalue("listtrait")
            if ctx:
                break
        res.parent = ctx
        print(res)

        return res
