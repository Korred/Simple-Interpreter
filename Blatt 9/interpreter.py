import py

from simpleparser import parse
from objmodel import W_Integer, W_Method, W_NormalObject


class Interpreter(object):

    def eval(self, ast, w_context):
        method = getattr(self, "eval_" + ast.__class__.__name__)
        return method(ast, w_context)

    def eval_Program(self, ast, w_context):
        print("### Evaluating program ###")
        print(ast)
        res = None
        for s in ast.statements:
            res = self.eval(s, w_context)
        return res

    def eval_Assignment(self, ast, w_context):
        print("### Evaluating assignment ###")
        print(ast)
        res = self.eval(ast.expression, w_context)
        w_context.setvalue(ast.attrname, res)
        return res

    def eval_IntLiteral(self, ast, w_context):
        return W_Integer(ast.value)

    def eval_IfStatement(self, ast, w_context):
        # or if else statement instead of try/except
        print("### Evaluating IFStatement ###")
        print(ast)
        try:
            condition = self.eval(ast.condition, w_context).istrue()
        except AttributeError:
            condition = False
        print(condition)

        if condition:
            return self.eval(ast.ifblock, w_context)
        else:
            return self.eval(ast.elseblock, w_context)

    def eval_MethodCall(self, ast, w_context):
        print("### Evaluating MethodCall ###")
        print(ast)
        if ast.receiver.__class__.__name__ == "ImplicitSelf":
            m = w_context.getvalue(ast.methodname)
            print(m.__class__.__name__)
            if m.__class__.__name__ == "W_Method":
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
        else:
            # some stuff for handling other recievers than ImplicitSelf
            pass
        ### stuff to handle 
        

    def eval_FunctionDefinition(self, ast, w_context):
        print("### FunctionDef ###")
        m = W_Method(ast.block)
        m.setvalue("args", ast.arguments)
        w_context.setvalue(ast.name, m)

    def eval_ExprStatement(self, ast, w_context):
        print("### Evaluating ExprStatement ###")
        res = self.eval(ast.expression, w_context)
        return res