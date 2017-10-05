import sys
from io import StringIO


class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.dict = dict()

    def __getitem__(self, key):
        cur = self
        while cur:
            if key in cur.dict:
                return cur.dict[key]
            cur = cur.parent

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if_lst = self.if_true if self.condition.evaluate(scope).value \
                 else self.if_false
        if not if_lst:
            return Number(0)
        res = None
        for expr in if_lst:
            res = expr.evaluate(scope)
        return res


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for arg_name, arg_value in zip(function.args, self.args):
            call_scope[arg_name] = arg_value.evaluate(scope)
        res = None
        for expr in function.body:
            res = expr.evaluate(call_scope)
        return res


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        a = self.lhs.evaluate(scope).value
        b = self.rhs.evaluate(scope).value
        op = self.op
        if op == '+':
            return Number(a + b)
        elif op == '-':
            return Number(a - b)
        elif op == '*':
            return Number(a * b)
        elif op == '/':
            return Number(a // b)
        elif op == '%':
            return Number(a % b)
        elif op == '==':
            return Number(int(a == b))
        elif op == '!=':
            return Number(int(a != b))
        elif op == '<':
            return Number(int(a < b))
        elif op == '>':
            return Number(int(a > b))
        elif op == '<=':
            return Number(int(a <= b))
        elif op == '>=':
            return Number(int(a >= b))
        elif op == '&&':
            return Number(int(a and b))
        elif op == '||':
            return Number(int(a or b))


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope).value
        op = self.op
        if op == '-':
            return Number(-a)
        elif op == '!':
            return Number(int(a == 0))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def BinaryOperationTests():
    scope = Scope()
    assert BinaryOperation(Number(1), '+',
                           Number(-2)).evaluate(scope) == Number(1 - 2)
    assert BinaryOperation(Number(1), '-',
                           Number(-2)).evaluate(scope) == Number(1 + 2)
    assert BinaryOperation(Number(1), '*',
                           Number(-2)).evaluate(scope) == Number(-2)
    assert BinaryOperation(Number(12), '/',
                           Number(5)).evaluate(scope) == Number(12 // 5)
    assert BinaryOperation(Number(12), '%',
                           Number(5)).evaluate(scope) == Number(12 % 5)

    assert BinaryOperation(Number(4), '==',
                           Number(5)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(4), '==',
                           Number(4)).evaluate(scope) == Number(1)

    assert BinaryOperation(Number(1), '!=',
                           Number(-2)).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(-2), '!=',
                           Number(-2)).evaluate(scope) == Number(0)

    assert BinaryOperation(Number(1), '<',
                           Number(-2)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(-2), '<',
                           Number(-2)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(-2), '<',
                           Number(1)).evaluate(scope) == Number(1)

    assert BinaryOperation(Number(1), '>',
                           Number(-2)).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(-2), '>',
                           Number(-2)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(-2), '>',
                           Number(1)).evaluate(scope) == Number(0)

    assert BinaryOperation(Number(1), '<=',
                           Number(-2)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(-2), '<=',
                           Number(-2)).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(-2), '<=',
                           Number(1)).evaluate(scope) == Number(1)

    assert BinaryOperation(Number(1), '>=',
                           Number(-2)).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(-2), '>=',
                           Number(-2)).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(-2), '>=',
                           Number(1)).evaluate(scope) == Number(0)

    assert BinaryOperation(Number(0), '&&',
                           Number(0)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(0), '&&',
                           Number(1)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(1), '&&',
                           Number(0)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(1), '&&',
                           Number(1)).evaluate(scope) == Number(1)

    assert BinaryOperation(Number(0), '||',
                           Number(0)).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(0), '||',
                           Number(1)).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(1), '||',
                           Number(0)).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(1), '||',
                           Number(1)).evaluate(scope) == Number(1)


def UnaryOperationTests():
    scope = Scope()
    assert UnaryOperation('!', Number(0)).evaluate(scope) == Number(1)
    assert UnaryOperation('!', Number(1)).evaluate(scope) == Number(0)

    assert UnaryOperation('-', Number(1)).evaluate(scope) == Number(-1)
    assert UnaryOperation('-', Number(-2)).evaluate(scope) == Number(2)


def PrintReadTests():
    scope = Scope()
    backupStdout = sys.stdout
    backupStdin = sys.stdin
    s = "2056789\n"
    sys.stdin = StringIO(s)
    sys.stdout = StringIO()

    Read('input').evaluate(scope)
    Print(Reference('input')).evaluate(scope)
    assert sys.stdout.getvalue() == s

    sys.stdout = backupStdout
    sys.stdin = backupStdin


def ConditionalTests():
        scope = Scope()
        backup = sys.stdout
        sys.stdout = StringIO()

        Conditional(Number(1), [Print(Number(1))],
                    [Print(Number(0))]).evaluate(scope)
        Conditional(Number(0), [Print(Number(1))],
                    [Print(Number(0))]).evaluate(scope)
        assert sys.stdout.getvalue() == "1\n0\n"

        sys.stdout = backup


def FunctionReferenceTests():
    scope = Scope()
    funcFirst = Function(["arg"], [BinaryOperation(Reference("arg"),
                                                   '*', Number(5))])
    FunctionDefinition("Five", funcFirst).evaluate(scope)
    assert FunctionCall(Reference("Five"),
                        [Number(42)]).evaluate(scope) == Number(210)

    funcSecond = Function(["arg"],
                          [FunctionDefinition("Five", funcFirst),
                           BinaryOperation(Reference("arg"), '*',
                                           FunctionCall(Reference("Five"),
                                                        [Number(2)]))])
    assert FunctionCall(FunctionDefinition('Ten', funcSecond),
                        [Number(3)]).evaluate(scope) == Number(30)


def my_tests():
    BinaryOperationTests()
    UnaryOperationTests()
    PrintReadTests()
    ConditionalTests()
    FunctionReferenceTests()


if __name__ == '__main__':
    example()
    my_tests()
