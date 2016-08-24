import py
import operator
from simpleparser import parse
from objmodel import W_Integer, W_Method, W_NormalObject
import default_builtins
import pdb


class Interpreter(object):

    def __init__(self,builtincode=None):
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



        ctx = self.eval(ast.lvalue, w_context)
        res = self.eval(ast.expression, ctx)
        ctx.setvalue(ast.attrname, res)


        return res

    def eval_IntLiteral(self, ast, w_context):



        res = W_Integer(ast.value)
        for i in w_context.getc3():
            ctx = i.getvalue("inttrait")
            if ctx:
                break
        res.parent=ctx

        return res

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


            # get lookup order (C3 MRO)








            for i in w_context.getc3():
                m = i.getvalue(ast.methodname)
                if m:
                    break


            if m.__class__.__name__ == "W_Method":
                m = m.clone()

                zipped_args = dict(zip(m.attrs["args"],ast.arguments))
                m.attrs.update(zipped_args)

                res = self.eval(m.method, m)


                return res
            elif m.__class__.__name__ == "IntLiteral":
                res = self.eval(m, w_context)
                return res
            elif m.__class__.__name__ == "W_Integer":

                return m
            elif m.__class__.__name__ == "W_NormalObject":
                return m
        else:
            # different receiver of methodcall

            rec = self.eval(ast.receiver,w_context)
            # eval reciever object



            #inttrait logic
            if rec.__class__.__name__ == "W_Integer":



                for i in w_context.getc3():
                    ctx = i.getvalue("inttrait")
                    if ctx:
                        break

                # "object found"
                m = ctx.getvalue(ast.methodname)

                if ast.arguments:

                    params = []
                    for p in ast.arguments:
                        # eval arguments as receiver later is different

                        if p.__class__.__name__ in ["W_NormalObject", "W_Integer", "W_Method"]:
                            params.append(p)
                        else:
                            # it might be necessary to handle different edge cases here
                            # or maybe not... should be tested accordingly
                            res = self.eval(p, w_context)
                            params.append(res)


                # case where is a W_Method object
                if m.__class__.__name__ == "W_Method":
                    m.setvalue("self", rec)
                    if ast.arguments:
                        zipped_args = dict(zip(m.attrs["args"], params))
                        m.attrs.update(zipped_args)

                    res = self.eval(m.method, m)
                    return res

                elif m.__class__.__name__ == "W_Integer":

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

                    if p.__class__.__name__ in ["W_NormalObject", "W_Integer", "W_Method"]:
                        params.append(p)
                    else:
                        # it might be necessary to handle different edge cases here
                        # or maybe not... should be tested accordingly
                        res = self.eval(p, w_context)
                        params.append(res)


            # case where is a W_Method object
            if m.__class__.__name__ == "W_Method":
                m.setvalue("self", rec)
                if ast.arguments:
                    zipped_args = dict(zip(m.attrs["args"], params))
                    m.attrs.update(zipped_args)

                res = self.eval(m.method, m)
                return res

            elif m.__class__.__name__ == "W_Integer":

                return m

            else:

                pass




        ### stuff to handle 
        

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
        if ast.methodname == "$int_add":
            op = operator.add
        elif ast.methodname == "$int_sub":
            op = operator.sub
        elif ast.methodname == "$int_mul":
            op = operator.mul
        elif ast.methodname == "$int_div":
            op = operator.truediv
        acc = self.eval(ast.receiver, w_context).value
        for e in ast.arguments:
            acc = op(acc, self.eval(e, w_context).value)
        return W_Integer(acc)

    def eval_WhileStatement(self, ast, w_context):
        res = None
        if not self.eval(ast.condition, w_context).istrue():
            res = self.eval(ast.elseblock, w_context)
        else:
            while self.eval(ast.condition, w_context).istrue():
                res = self.eval(ast.whileblock, w_context)
        return res

    def eval_ImplicitSelf(self,ast, w_context):
        return w_context