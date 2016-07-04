import py
import operator
from simpleparser import parse
from objmodel import W_Integer, W_Method, W_NormalObject


class Interpreter(object):

    def eval(self, ast, w_context):
        print(w_context)
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
        print(ast)
        res = self.eval(ast.expression, w_context)
        w_context.setvalue(ast.attrname, res)
        print("ASSIGN", ast.attrname, res)
        return res

    def eval_IntLiteral(self, ast, w_context):
        print()
        print("### Evaluating IntLiteral ###")
        print(W_Integer(ast.value).value)
        return W_Integer(ast.value)

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
        print(ast)
        if ast.receiver.__class__.__name__ == "ImplicitSelf":
            print("RECIEVER = IMPLICITSELF")
            print(w_context.attrs)
            # get lookup order (C3 MRO)

            print(ast.methodname)
            print(w_context)
            print("PARENTS", w_context.getparents())
            print("PARENTS", w_context.parents)
            print("MRO LIST ", w_context.getc3())

            print("CHECKING MRO")
            for i in w_context.getc3():
                m = i.getvalue(ast.methodname)
                if m:
                    break

            print("FOUND:", m.__class__.__name__)
            if m.__class__.__name__ == "W_Method":
                m = m.clone()
                print(m.attrs)
                zipped_args = dict(zip(m.attrs["args"],ast.arguments))
                m.attrs.update(zipped_args)
                print(m.attrs)
                res = self.eval(m.method, m)
                print(res)

                return res
            elif m.__class__.__name__ == "IntLiteral":
                res = self.eval(m, w_context)
                return res
            elif m.__class__.__name__ == "W_Integer":
                return m
            elif m.__class__.__name__ == "W_NormalObject":
                return m
        else:
            # different reciever of methodcall
            print("RECIEVER =",ast.receiver.methodname)
            # getting reciever from w_context
            rec = self.eval(ast.receiver,w_context)
            print(2,rec)
            print(3,rec.attrs)

            # get method by methodname from reciever rec
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
                    # eval arguments as reciever later is different
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




        ### stuff to handle 
        

    def eval_FunctionDefinition(self, ast, w_context):
        print()
        print("### Evaluating FunctionDef ###")
        print(ast)
        print(ast.block)
        m = W_Method(ast.block)
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

    # by now we just create an empty W_NormalObject
    def make_module(self):
        return W_NormalObject()

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
