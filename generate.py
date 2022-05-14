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

def symbol_add_sub(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    left = signed_add_sub(level)
    right = generator.generate_ranged()
    utils.replace_one_symbol(left)
    return utils.Equation(left, right)

def symbol_add_sub2(level):
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

def mix_asmd():
    generator = utils.Generator(maximum=_maximum_on_level(1), signed=True)
    def operator(): return np.random.choice([utils.Add, utils.Sub, utils.Mul, utils.Div])
    def subroot(): return operator()(generator.generate_ranged(), generator.generate_ranged())
    left, right = [generator.generate_ranged() if np.random.ranf() < 0.5 else subroot() for _ in range(2)]
    return operator()(left, right)

def factor(num_factors):
    generator = utils.Generator(prime_factors=num_factors, signed=False)
    return generator.generate_factored()

def div_factor(num_factors):
    generator = utils.Generator(prime_factors=num_factors, signed=False)
    return utils.Div(generator.generate_factored(), generator.generate_factored())

def gcd_and_lcm(num_factors):
    generator = utils.Generator(prime_factors=num_factors, signed=False)
    a = generator.generate_factored()
    b = generator.generate_factored()
    return utils.Gcd(a, b) if np.random.ranf() < 0.5 else utils.Lcm(a, b)

def symbol_mul_div(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a = generator.generate_ranged()
    b = generator.generate_ranged(nonzero=True)
    left = np.random.choice([utils.Mul, utils.Div])(a, b)
    right = generator.generate_ranged()
    utils.replace_one_symbol(left)
    return utils.Equation(left, right)

def rational_symbol_mul_div(level):
    generator = utils.Generator(prime_factors=level, signed=True)
    left = _generate_symbol_with_cofficent(np.random.choice(list('abcxyz')), level, np.random.ranf() < 0.5)
    right = _generate_rational(level) if np.random.ranf() < 0.5 else generator.generate_factored()
    return utils.Equation(left, right)

def rational_symbol_mul_div2(level):
    def operator(): return np.random.choice([utils.Add, utils.Sub])
    def operand(): return _generate_rational(level) if np.random.ranf() < 0.5 else generator.generate_factored()
    generator = utils.Generator(prime_factors=level, signed=True)
    symbol = np.random.choice(list('abcxyz'))
    left = _generate_symbol_with_cofficent(symbol, level, np.random.ranf() < 0.5)
    left = operator()(left, operand() if np.random.ranf() < 0.5 else _generate_symbol_with_cofficent(symbol, level, np.random.ranf() < 0.5))
    right = operand()
    return utils.Equation(left, right)

def simple_rational(num_factors, num_operators=2, operations=(utils.Add, utils.Sub)):
    generator = utils.Generator(prime_factors=num_factors, signed=True)
    def factors(): return [generator.generate_factored() for _ in range(2)]
    def operand(): return np.random.choice([utils.Positive, utils.Negative])(utils.Div(*factors()))
    def operator(): return np.random.choice(operations)
    root = operand()
    for _ in range(1, num_operators): root = operator()(root, operand())
    return root

def rational_comparison(level):
    def _method0(num, shift): return utils.Div(num - shift, num), utils.Div(num, num + shift)
    def _method1(num, shift): return utils.Div(1, num), utils.Div(1, num + shift)
    generator = utils.Generator(maximum=_maximum_on_level(level))
    num = abs(generator.generate_ranged(True))
    a, b = np.random.choice([_method0, _method1])(num, np.random.randint(1, 4))
    if np.random.ranf() < 0.5: a, b = b, a
    if np.random.ranf() < 0.5: a, b = utils.Negative(a), utils.Negative(b)
    return utils.Compare(a, b)

def symbol_rational(num_factors, num_operators=2):
    generator = utils.Generator(prime_factors=num_factors, signed=True)
    a = generator.generate_factored()
    b = generator.generate_factored()
    left = simple_rational(num_factors, num_operators)
    right = utils.Div(a, b)
    utils.replace_one_symbol(left)
    return utils.Equation(left, right)

def linear_equations(num_variables, level):
    symbol_sets = np.random.choice(['abcdef', 'uvwxyz'])
    symbols = symbol_sets[:num_variables]
    equations = []
    for _ in range(num_variables):
        equation = _generate_linear_equation(symbols, level)
        equations.append(equation)
    return utils.EquationSet(equations)

def _maximum_on_level(level):
    if level == 0: maximum = 9
    elif level == 1: maximum = 99
    elif level == 2: maximum = 99999
    return maximum

def _generate_symbol_with_cofficent(symbol, level, rational=True):
    if rational:
        cofficient = _generate_rational(level)
    else:
        generator = utils.Generator(prime_factors=level, signed=True)
        cofficient = generator.generate_factored()
    return utils.Mul(cofficient, symbol)

def _generate_linear_equation(symbols, level):
    generator = utils.Generator(prime_factors=level, signed=True)
    left = None
    for x in symbols:
        token = _generate_symbol_with_cofficent(x, level)
        if left is None: left = token
        else: left = np.random.choice([utils.Add, utils.Sub])(left, token)
    right = generator.generate_factored()
    return utils.Equation(left, right)

def _generate_rational(level):
    generator = utils.Generator(prime_factors=level, signed=True)
    return utils.Div(generator.generate_factored(), generator.generate_factored())

if __name__ == '__main__':
    pg = utils.ProblemGenerator(rational_comparison, 1, count=30)
    pg.generate()