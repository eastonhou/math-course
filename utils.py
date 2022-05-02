import numpy as np

class Generator:
    def __init__(self, prime_numbers=[2, 3, 5, 7, 11, 13], prime_factors=3, maximum=200, signed=True):
        self.prime_numbers = prime_numbers
        self.prime_factors = prime_factors,
        self.maximum = maximum
        self.signed = signed

    def generate_ranged(self, nonzero=False):
        if self.signed: result = np.random.randint(-self.maximum, self.maximum + 1)
        else: result = np.random.randint(0, self.maximum + 1)
        if result == 0 and nonzero: return self.generate_ranged(nonzero=nonzero)
        else: return result

    def generate_factored(self):
        factors = np.random.choice(self.prime_numbers, self.prime_factors)
        return np.prod(factors)

class ProblemGenerator:
    def __init__(self, method, *args, count=20, **kwargs) -> None:
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.count = count

    def generate(self, deliminator=None):
        for _ in range(self.count):
            if deliminator is not None: print(deliminator)
            print(self.method(*self.args, **self.kwargs))

class Expression:
    PRIORITY_NUMBER = 0
    PRIORITY_SIGN = 3
    PRIORITY_FUNCTION = 1
    PRIORITY_MULTIPLICATION = 2
    PRIORITY_ADD = 3
    def __init__(self, operator, priority, *values):
        self.operator = operator
        self.priority = priority
        self.values = list(values)

    @property
    def value(self): return self.values[0]

    def __neg__(self):
        return Negative(self)

class SingleValueExpression(Expression):
    def __str__(self) -> str:
        right = f'({str(self.value)})' if self.value.priority >= self.priority else str(self.value)
        return self.operator + right

class TwoSideExpression(Expression):
    def __str__(self) -> str:
        left, right = self.values
        right = f'({str(right)})' if right.priority >= self.priority else str(right)
        left = str(left) if left.priority <= self.priority or isinstance(left, SingleValueExpression) else f'({str(left)})'
        return left + self.operator + right

class Positive(Expression):
    def __init__(self, value):
        super().__init__('', __class__.PRIORITY_NUMBER, value)

    def __str__(self) -> str:
        return str(self.value)

    def evaluate(self):
        return self.value.evaluate() if isinstance(self.value, Expression) else self.value

class Negative(SingleValueExpression):
    def __init__(self, value):
        super().__init__('-', __class__.PRIORITY_SIGN, autoexpr(value))

    def evaluate(self):
        return -self.values[0].evaluate()

class Symbol(Expression):
    def __init__(self, value):
        super().__init__('', __class__.PRIORITY_NUMBER, value)

    def __str__(self) -> str:
        return self.value

class Function(Expression):
    def __init__(self, operator, *values):
        super().__init__(operator, __class__.PRIORITY_FUNCTION, *values)

class Mul(TwoSideExpression):
    def __init__(self, a, b):
        super().__init__('*', __class__.PRIORITY_MULTIPLICATION, autoexpr(a), autoexpr(b))

    def evaluate(self):
        return self.values[0].evaluate() * self.values[1].evaluate()

class Div(TwoSideExpression):
    def __init__(self, a, b):
        super().__init__('/', __class__.PRIORITY_MULTIPLICATION, autoexpr(a), autoexpr(b))

    def evaluate(self):
        return self.values[0].evaluate() / self.values[1].evaluate()

class Add(TwoSideExpression):
    def __init__(self, a, b):
        super().__init__('+', __class__.PRIORITY_ADD, autoexpr(a), autoexpr(b))

    def evaluate(self):
        return self.values[0].evaluate() + self.values[1].evaluate()

class Sub(TwoSideExpression):
    def __init__(self, a, b):
        super().__init__('-', __class__.PRIORITY_ADD, autoexpr(a), autoexpr(b))

    def evaluate(self):
        return self.values[0].evaluate() - self.values[1].evaluate()

class Gcd(Expression):
    def __init__(self, *values):
        super().__init__('gcd', __class__.PRIORITY_FUNCTION, *[autoexpr(x) for x in values])

    def __str__(self):
        return f'({",".join([str(x) for x in self.values])})'

    def evaluate(self):
        out = 1
        for v in self.values: out = np.gcd(out, v.evaluate())

class Lcm(Expression):
    def __init__(self, *values):
        super().__init__('gcd', __class__.PRIORITY_FUNCTION, *[autoexpr(x) for x in values])

    def __str__(self):
        return f'[{",".join([str(x) for x in self.values])}]'
        
    def evaluate(self):
        out = 1
        for v in self.values: out = np.lcm(out, v.evaluate())

class Equation:
    def __init__(self, left, right) -> None:
        self.left = autoexpr(left)
        self.right = autoexpr(right)

    def __str__(self) -> str:
        return str(self.left) + '=' + str(self.right)

class EquationSet:
    def __init__(self, equations):
        self.equations = equations

    def __str__(self):
        return '\n'.join([str(x) for x in self.equations])

def autoexpr(v):
    if isinstance(v, Expression): return v
    elif isinstance(v, str): return Symbol(v)
    else: return Positive(v) if v >= 0 else Negative(-v)

def collect_values(expr):
    def collect(root, values):
        if isinstance(root, Expression):
            for child in root.values:
                collect(child, values)
        else:
            values.append(root)
    values = []
    collect(expr, values)
    return values

def replace_values(expr, values):
    def replace(root, values):
        for i,child in enumerate(root.values):
            if isinstance(child, Expression):
                replace(child, values)
            else:
                root.values[i] = values.pop(0)
    replace(expr, values[:])

def replace_one_symbol(expr):
    values = collect_values(expr)
    symbol = np.random.choice(['a', 'b', 'c', 'd', 'x', 'y'])
    idx = np.random.choice(len(values))
    values[idx] = Symbol(symbol)
    replace_values(expr, values)
    return expr
