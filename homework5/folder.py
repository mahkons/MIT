from yat.model import *
from io import StringIO


class ConstantFolder:
    def __init__(self):
        self.op_scope = Scope()

    def visit(self, tree):
        return tree.accept(self)

    def visitNumber(self, number):
        return number

    def visitFunctionDefinition(self, fd):
        for expr in fd.function.body:
            expr = self.visit(expr)
        return fd

    def visitConditional(self, conditional):
        for expr in fd.function.body:
            expr = self.visit(expr)
        conditional.condition = self.visit(condition)
        for expr in conditional.if_true:
            expr = self.visit(expr)
        for expr in conditional.if_false:
            expr = self.visit(expr)
        return conditional

    def visitPrint(self, expr):
        return Print(self.visit(expr))

    def visitRead(self, expr):
        return Read(self.visit(expr))

    def visitFunctionCall(self, fc):
        for expr in fc.args:
            expr = self.visit(expr)
        return expr

    def visitReference(self, reference):
        return reference

    def visitBinaryOperation(self, op):
        op.lhs = self.visit(op.lhs)
        op.rhs = self.visit(op.rhs)
        if isinstance(op.lhs, Number) and isinstance(op.rhs, Number):
            return op.evaluate(self.op_scope)
        if op.op == '*' and ((isinstance(op.lhs, Number) and
                              op.lhs.value == 0 and
                              isinstance(op.rhs, Reference)) or
                             (isinstance(op.rhs, Number) and
                              op.rhs.value == 0 and
                              isinstance(op.lhs, Reference))):
            return Number(0)
        if op.op == '-' and isinstance(op.lhs, Reference) and \
           isinstance(op.rhs, Reference) and op.lhs.name == op.lhs.name:
            return Number(0)

    def visitUnaryOperation(self, op):
        op.expr = self.visit(op.expr)
        if isinstance(op.expr, Number):
            return op.evaluate(self.op_scope)


def my_tests():
    folder = ConstantFolder()
    assert folder.visit(BinaryOperation(Reference('world'),
                                        '-', Reference('world'))) == Number(0)
    assert folder.visit(BinaryOperation(Number(0),
                                        '*', Reference('world'))) == Number(0)
    assert folder.visit(BinaryOperation(Reference('world'),
                                        '*', Number(0))) == Number(0)
    assert folder.visit(BinaryOperation(Number(7),
                                        '/', Number(2))) == Number(3)
    assert folder.visit(UnaryOperation('-',
                                       Number(-3))) == Number(3)


if __name__ == '__main__':
    my_tests()
