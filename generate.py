from torch import maximum
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
    return utils.Add(a, b) if np.random.ranf() < 0.5 else utils.Sub(a, b)

def signed_add_sub2(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    root = utils.Add if np.random.ranf() < 0.5 else utils.Sub
    left, right = [generator.generate_ranged() if np.random.ranf() < 0.5 else signed_add_sub(level) for _ in range(2)]
    return root(left, right)

def mul(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a, b = [generator.generate_ranged() for _ in range(2)]
    return utils.Mul(a, b)

def div(level):
    generator = utils.Generator(maximum=_maximum_on_level(level), signed=True)
    a, b = [generator.generate_ranged() for _ in range(2)]
    if b == 0: b = 1
    return utils.Div(a, b)

def mul_div():
    generator = utils.Generator(maximum=_maximum_on_level(2), signed=True)
    a = generator.generate_ranged()
    b = generator.generate_ranged(nonzero=True)
    root = utils.Mul if np.random.ranf() < 0.5 else utils.Div
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

def simple_rational(num_factors):
    generator = utils.Generator(prime_factors=num_factors, signed=True)
    def factors(): return [generator.generate_factored() for _ in range(2)]
    def operand(): return np.random.choice([utils.Positive, utils.Negative])(utils.Div(*factors()))
    root = np.random.choice([utils.Add, utils.Sub])(operand(), operand())
    return root

def _maximum_on_level(level):
    if level == 0: maximum = 9
    elif level == 1: maximum = 99
    elif level == 2: maximum = 99999
    return maximum

if __name__ == '__main__':
    pg = utils.ProblemGenerator(simple_rational, 2)
    pg.generate()