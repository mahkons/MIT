from yat.model import *
from io import StringIO


class PrettyPrinter:
    def __init__(self, add=4):
        self.spaces = 0
        self.add = add
        self.statement = True

    def print_spaces(self):
        print(' ' * self.spaces, end='')

    def enter(self):
        self.spaces += self.add
        print('{', end='\n')

    def exit(self):
        self.spaces -= self.add
        self.print_spaces()
        print('}', end='')

    def visit(self, tree):
        if self.statement:
            self.print_spaces()
        tree.accept(self)
        if self.statement:
            print(';')

    def visitConditional(self, conditional):
        print('if (', end='')

        self.statement = False
        self.visit(conditional.condition)
        self.statement = True

        print(') ', end='')

        self.enter()
        for expr in conditional.if_true:
            self.visit(expr)
        self.exit()

        print(' else ', end='')
        self.enter()
        for expr in conditional.if_false:
            self.visit(expr)
        self.exit()

    def visitFunctionDefinition(self, fd):
        print('def ', end='')
        print(fd.name, '(', ', '.join(fd.function.args), ') ', sep='', end='')

        self.enter()
        for statement in fd.function.body:
            self.visit(statement)
        self.exit()

    def visitPrint(self, stat):
        print('print ', end='')
        self.statement = False
        self.visit(stat.expr)
        self.statement = True

    def visitRead(self, stat):
        print('read ', end='')
        print(stat.name, end='')

    def visitNumber(self, number):
        print(number.value, end='')

    def visitReference(self, reference):
        print(reference.name, end='')

    def visitBinaryOperation(self, op):
        print('(', end='')

        save_statement = self.statement
        self.statement = False

        print('(', end='')
        self.visit(op.lhs)
        print(')', end='')

        print(op.op, end='')

        print('(', end='')
        self.visit(op.rhs)
        print(')', end='')

        self.statement = save_statement

        print(')', end='')

    def visitUnaryOperation(self, op):
        print('(', end='')

        save_statement = self.statement
        self.statement = False

        print('(', end='')
        print(op.op, end='')

        self.visit(op.expr)
        print(')', end='')

        self.statement = save_statement

        print(')', end='')

    def visitFunctionCall(self, fn):
        save_statement = self.statement
        self.statement = False
        self.visit(fn.fun_expr)

        print('(', end='')
        if fn.args:
            self.visit(fn.args[0])
            for arg in fn.args[1:]:
                print(', ', end='')
                self.visit(arg)
        print(')', end='')
        self.statement = save_statement


def func_test():

    backupStdout = sys.stdout
    sys.stdout = StringIO()

    scope = Scope()

    printer = PrettyPrinter()
    funcFirst = Function(["arg"], [BinaryOperation(Reference("arg"),
                                                   '*', Number(5))])
    printer.visit(FunctionDefinition("Five", funcFirst))
    printer.visit(FunctionCall(Reference("Five"),
                               [Number(42)]))

    printer.visit(FunctionDefinition("Five", funcFirst))
    printer.visit(BinaryOperation(Reference("arg"), '*',
                                  FunctionCall(Reference("Five"),
                                               [Number(2)])))

    assert sys.stdout.getvalue() == """def Five(arg) {
    ((arg)*(5));
};
Five(42);
def Five(arg) {
    ((arg)*(5));
};
((arg)*(Five(2)));
"""
    sys.stdout = backupStdout


def conditional_test():
    scope = Scope()
    backup = sys.stdout
    sys.stdout = StringIO()

    printer = PrettyPrinter()
    printer.visit(Conditional(Number(1), [Print(Number(1))],
                              [Print(Number(0))]))
    printer.visit(Conditional(Number(0), [Print(Number(1))],
                              [Print(Number(0))]))
    assert sys.stdout.getvalue() == """if (1) {
    print 1;
} else {
    print 0;
};
if (0) {
    print 1;
} else {
    print 0;
};
"""

    sys.stdout = backup


def op_test():
    scope = Scope()
    backup = sys.stdout
    sys.stdout = StringIO()

    printer = PrettyPrinter()
    printer.visit(UnaryOperation('!', Number(0)))
    printer.visit(UnaryOperation('-', Number(1)))
    printer.visit(BinaryOperation(Number(0), '||', Number(1)))
    printer.visit(BinaryOperation(Number(-1), '>=', Number(2)))
    assert sys.stdout.getvalue() == """((!0));
((-1));
((0)||(1));
((-1)>=(2));
"""

    sys.stdout = backup


def my_tests():
    func_test()
    conditional_test()
    op_test()


if __name__ == '__main__':
    my_tests()
