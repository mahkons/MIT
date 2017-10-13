import sys 

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
    
    def accept(self, visitor):
        return visitor.visitNumber(self)


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

    def accept(self, visitor):
        return visitor.visitFunctionDefinition(self)


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

    def accept(self, visitor):
        return visitor.visitConditional(self)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)

    def accept(self, visitor):
        return visitor.visitPrint(self)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))

    def accept(self, visitor):
        return visitor.visitRead(self)


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

    def accept(self, visitor):
        return visitor.visitFunctionCall(self)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visitReference(self)


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

    def accept(self, visitor):
        return visitor.visitBinaryOperation(self)


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

    def accept(self, visitor):
        return visitor.visitUnaryOperation(self)

