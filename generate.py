import utils
import numpy as np

def unsigned_add(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=False)
    a, b = [generator.generate_ranged() for _ in range(2)]
    return utils.Add(a, b)

def unsigned_sub(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=False)
    a, b = [generator.generate_ranged() for _ in range(2)]
    return utils.Sub(a + b, a)

def signed_add_sub(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a, b = [generator.generate_ranged() for _ in range(2)]
    return np.random.choice([utils.Add, utils.Sub])(a, b)

def signed_add_sub2(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    root = np.random.choice([utils.Add, utils.Sub])
    left, right = [generator.generate_ranged() if np.random.ranf() < 0.5 else signed_add_sub(level) for _ in range(2)]
    return root(left, right)

def add_sub_equation(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    left = signed_add_sub(level)
    right = generator.generate_ranged()
    utils.replace_one_symbol(left)
    return utils.Equation(left, right)

def add_sub_equation2(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    left = signed_add_sub2(level)
    right = generator.generate_ranged()
    utils.replace_one_symbol(left)
    return utils.Equation(left, right)

def mul(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a, b = [generator.generate_ranged() for _ in range(2)]
    return utils.Mul(a, b)

def div(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a, b = [generator.generate_ranged() for _ in range(2)]
    if b == 0: b = 1
    return utils.Div(a, b)

def mul_div(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a = generator.generate_ranged()
    b = generator.generate_ranged(nonzero=True)
    root = np.random.choice([utils.Mul, utils.Div])
    return root(a/100, b/100)

def mix_arithmetic():
    generator = utils.Generator(maximum=_maximum_on_level(1), signed=True)
    def operator(): return np.random.choice([utils.Add, utils.Sub, utils.Mul, utils.Div])
    def subroot(): return operator()(generator.generate_ranged(), generator.generate_ranged())
    left, right = [generator.generate_ranged() if np.random.ranf() < 0.5 else subroot() for _ in range(2)]
    return operator()(left, right)

def factor(num_factors):
    generator = utils.Generator(prime_factors=num_factors, signed=False)
    return generator.generate_factored()

def simplify(num_factors):
    generator = utils.Generator(prime_factors=num_factors, signed=False)
    return utils.Div(generator.generate_factored(), generator.generate_factored())

def gcd_and_lcm(num_factors):
    generator = utils.Generator(prime_factors=num_factors, signed=False)
    a = generator.generate_factored()
    b = generator.generate_factored()
    return utils.Gcd(a, b) if np.random.ranf() < 0.5 else utils.Lcm(a, b)

def mul_div_equation(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a = generator.generate_ranged()
    b = generator.generate_ranged(nonzero=True)
    left = np.random.choice([utils.Mul, utils.Div])(a, b)
    right = generator.generate_ranged()
    utils.replace_one_symbol(left)
    return utils.Equation(left, right)

def simple_rational(num_factors, num_operators=2, operations=(utils.Add, utils.Sub)):
    generator = utils.Generator(prime_factors=num_factors, signed=True)
    def factors(): return [generator.generate_factored() for _ in range(2)]
    def operand(): return np.random.choice([utils.Positive, utils.Negative])(utils.Div(*factors()))
    def operator(): return np.random.choice(operations)
    root = operand()
    for _ in range(1, num_operators): root = operator()(root, operand())
    return root

def simple_rational_equation(level):
    generator = utils.Generator(prime_factors=level, signed=True)
    left = _generate_symbol_with_cofficent(np.random.choice(list('abcxyz')), level, np.random.ranf() < 0.5)
    right = _generate_rational(level) if np.random.ranf() < 0.5 else generator.generate_factored()
    return utils.Equation(left, right)

def rational_equation(num_factors, num_operators=2):
    generator = utils.Generator(prime_factors=num_factors, signed=True)
    a = generator.generate_factored()
    b = generator.generate_factored()
    left = simple_rational(num_factors, num_operators)
    right = utils.Div(a, b)
    utils.replace_one_symbol(left)
    return utils.Equation(left, right)

def rational_equation2(level):
    def operator(): return np.random.choice([utils.Add, utils.Sub])
    def operand(): return _generate_rational(level) if np.random.ranf() < 0.5 else generator.generate_factored()
    generator = utils.Generator(prime_factors=level, signed=True)
    symbol = np.random.choice(list('abcxyz'))
    left = _generate_symbol_with_cofficent(symbol, level, np.random.ranf() < 0.5)
    left = operator()(left, operand() if np.random.ranf() < 0.5 else _generate_symbol_with_cofficent(symbol, level, np.random.ranf() < 0.5))
    right = operand()
    return utils.Equation(left, right)

def rational_comparison(level):
    def _method0(num, shift): return utils.Div(num - shift, num), utils.Div(num, num + shift)
    def _method1(num, shift): return utils.Div(1, num), utils.Div(1, num + shift)
    generator = utils.Generator(maximum=_maximum_on_level(level))
    num = abs(generator.generate_ranged(True))
    a, b = np.random.choice([_method0, _method1])(num, np.random.randint(1, 4))
    if np.random.ranf() < 0.5: a, b = b, a
    if np.random.ranf() < 0.5: a, b = utils.Negative(a), utils.Negative(b)
    return utils.Compare(a, b)

def integral_linear_equations(num_variables, level):
    vmax = _maximum_on_level(level)
    symbol_set = np.random.choice(['abcdef', 'uvwxyz'])
    generator = utils.Generator(maximum=vmax)
    variables = [generator.generate_ranged() for _ in range(num_variables)]
    while True:
        mat = np.random.randint(-vmax, vmax + 1, size=(num_variables, num_variables))
        if np.linalg.det(mat) != 0: break
    ys = mat @ variables
    equations = []
    for coffs, y in zip(mat, ys):
        equations.append(_make_linear_equation(symbol_set[:num_variables], coffs, y))
    return utils.EquationSet(equations)

def linear_equations(num_variables, level, rational):
    symbol_set = np.random.choice(['abcdef', 'uvwxyz'])
    symbols = symbol_set[:num_variables]
    equations = []
    for _ in range(num_variables):
        equation = _generate_linear_equation(symbols, level, rational)
        equations.append(equation)
    return utils.EquationSet(equations)

def _maximum_on_level(level):
    if level == 0: maximum = 9
    elif level == 1: maximum = 99
    elif level == 2: maximum = 99999
    return maximum

def _generate_symbol_with_cofficent(symbol, level, rational):
    if rational:
        cofficient = _generate_rational(level)
    else:
        generator = utils.Generator(prime_factors=level, signed=True)
        cofficient = generator.generate_factored()
    return utils.Mul(cofficient, symbol)

def _generate_linear_equation(symbols, level, rational):
    generator = utils.Generator(prime_factors=level, signed=True)
    left = None
    for x in symbols:
        token = _generate_symbol_with_cofficent(x, level, rational)
        if left is None: left = token
        else: left = np.random.choice([utils.Add, utils.Sub])(left, token)
    right = generator.generate_factored()
    return utils.Equation(left, right)

def _make_linear_equation(symbols, coffcients, value):
    left = None
    for c, x in zip(coffcients, symbols):
        token = utils.Mul(c, x)
        if left is None: left = token
        else: left = utils.Add(left, token)
    return utils.Equation(left, value)

def _generate_rational(level):
    generator = utils.Generator(prime_factors=level, signed=True)
    return utils.Div(generator.generate_factored(), generator.generate_factored())

def generate_mix():
    np.random.seed(5001)
    print('一、混合加减乘除')
    utils.ProblemGenerator(mix_arithmetic, count=2).generate()
    print('二、带未知数加减')
    utils.ProblemGenerator(add_sub_equation2, 2, count=4).generate()
    print('三、分解素因子')
    utils.ProblemGenerator(factor, 3, count=4).generate()
    print('四、化简分数')
    utils.ProblemGenerator(simplify, 3, count=4).generate()
    print('五、最大公约数和最小公倍数')
    utils.ProblemGenerator(gcd_and_lcm, 3, count=4).generate()
    print('六、有理数加减乘除')
    utils.ProblemGenerator(simple_rational, 2, 3, (utils.Add, utils.Sub, utils.Mul, utils.Div), count=4).generate()
    print('七、求未知数')
    utils.ProblemGenerator(simple_rational_equation, 2, count=2).generate()
    utils.ProblemGenerator(rational_equation2, 1, count=2).generate()
    utils.ProblemGenerator(rational_equation, 2, 2, count=2).generate()
    print('八、有理数比大小')
    utils.ProblemGenerator(rational_comparison, 2, count=2).generate()
    print('九、解方程组')
    utils.ProblemGenerator(integral_linear_equations, 2, 0, count=2).generate('--------------')
    
if __name__ == '__main__':
    generate_mix()
