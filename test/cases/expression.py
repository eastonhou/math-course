from test import testutils as tu
from utils import *

class TestExpression(tu.TestBase):
    def test_add_sub(self):
        self.assertExpr(Add(5, 6), '5+6')
        self.assertExpr(Add(-5, 6), '-5+6')
        self.assertExpr(Add(5, -6), '5+(-6)')
        self.assertExpr(Sub(5, -6), '5-(-6)')
        self.assertExpr(Sub(-5, 6), '-5-6')
        self.assertExpr(Sub(-5, -6), '-5-(-6)')

    def test_mul_div(self):
        self.assertExpr(Mul(3, Div(4, 5)), '3*(4/5)')
        self.assertExpr(Mul(Div(4, 5), 3), '4/5*3')
        self.assertExpr(Div(4, -3), '4/(-3)')
        self.assertExpr(Div(-4, 3), '-4/3')

    def test_mix(self):
        self.assertExpr(Mul(12, Add(3, 4)), '12*(3+4)')
        self.assertExpr(Mul(12, Add(3, -4)), '12*(3+(-4))')
        self.assertExpr(Sub(12, Div(3, -4)), '12-3/(-4)')
        self.assertExpr(Sub(12, -Div(3, -4)), '12-(-3/(-4))')
        self.assertExpr(Add(12, Div(3, -4)), '12+3/(-4)')

    def assertExpr(self, expr, target):
        self.assertEqual(str(expr), target)
