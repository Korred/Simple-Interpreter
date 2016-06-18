import py

from simpleparser import parse
from objmodel import W_NormalObject, W_Integer


class Interpreter(object):

    def eval(self, ast, w_context):
        method = getattr(self, "eval_" + ast.__class__.__name__)
        return method(ast, w_context)

    def eval_Program(self, ast, w_context):
        print("### Evaluating program ###")
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
        try:
            condition = self.eval(ast.condition, w_context).istrue()
        except AttributeError:
            condition = False

        if condition:
            return self.eval(ast.ifblock, w_context)
        else:
            return self.eval(ast.elseblock, w_context)

    def eval_MethodCall(self, ast, w_context):
        if ast.receiver.__class__.__name__ == "ImplicitSelf":
            return w_context.getvalue(ast.methodname)

    def eval_FunctionDefinition(self, ast, w_context):
        print(ast.name)
        print(ast.arguments)
        print(ast.block)


# for testing purposes
ast = parse("""
def f(x, y):
    if x:
        x
    else:
        y
i = f(6, 3)
j = f(0, 9)
""")
w_module = W_NormalObject()
interpreter = Interpreter()
interpreter.eval(ast, w_module)
assert w_module.getvalue("i").value == 6
assert w_module.getvalue("j").value == 9
