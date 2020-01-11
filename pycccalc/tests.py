from calculator import Calculator

import unittest
import math
from functools import reduce


class TestCalculator(unittest.TestCase):
    """Some basic tests. Coverage incomplete."""

    def setUp(self):
        self.calc = Calculator()
        self.calc.functions = {
            'abs': abs,
            'pow': math.pow,
            'sin': math.sin
        }

    def helper(self, expression, success, correct_result=0):
        test_result = self.calc.evaluate(expression).result
        if success:
            self.assertEqual(test_result, correct_result)
        self.assertEqual(self.calc.success, success)

    def test_normal_addition(self):
        expression = "1+2"
        self.helper(expression, True, eval(expression))

    def test_normal_substraction(self):
        expression = "8-4"
        self.helper(expression, True, eval(expression))

    def test_big_addition(self):
        expression = "12892389238238238238789372891+22823892382382388233894789"
        self.helper(expression, True, eval(expression))

    def test_addition_with_brackets_1(self):
        expression = "(42+24)+2"
        self.helper(expression, True, eval(expression))

    def test_addition_with_brackets_2(self):
        expression = "2+(42+24)"
        self.helper(expression, True, eval(expression))

    def test_order_of_operations_1(self):
        expression = "7+7*2"
        self.helper(expression, True, eval(expression))

    def test_order_of_operations_2(self):
        expression = "77*2+3"
        self.helper(expression, True, eval(expression))

    def test_order_of_operations_3(self):
        expression = "(7+7)*2"
        self.helper(expression, True, eval(expression))

    def test_extensive_nesting(self):
        expression = "((((((23239*23+23)+2398)+12)*2)-2323*23)+23)"
        self.helper(expression, True, eval(expression))

    def test_spaces(self):
        expression = "    (2     +  5)    *    3    "
        self.helper(expression, True, eval(expression))

    def test_variables(self):
        self.calc.variables = {'obEcc': 0.244, 'smAxis': 39.2}
        expression = "smAxis*(1+obEcc)"
        variables = self.calc.variables
        self.helper(
            expression,
            True,
            eval(reduce(lambda e, v: e.replace(
                v, str(variables[v])), variables, expression
            ))
        )

    def test_functions(self):
        expression = "sin(18)+pow(3,4)"
        functions = self.calc.functions
        self.helper(
            expression,
            True,
            eval(reduce(lambda e, v: e.replace(
                v, "math." + v), functions, expression
            ).replace("math.abs", "abs"))
        )

    def test_nested_functions(self):
        expression = "pow(pow(2,abs(-2)),2)"
        functions = self.calc.functions
        self.helper(
            expression,
            True,
            eval(reduce(lambda e, v: e.replace(
                v, "math." + v), functions, expression
            ).replace("math.abs", "abs"))
        )

    def test_invalid_syntax_1(self):
        expression = "((10100"
        self.helper(expression, False)

    def test_invalid_syntax_2(self):
        expression = "10100+3)"
        self.helper(expression, False)

    def test_invalid_syntax_3(self):
        expression = "pow(pow(2,5)"
        self.helper(expression, False)

    def test_invalid_syntax_4(self):
        expression = "pow(pow(2,5)))"
        self.helper(expression, False)

    def test_invalid_syntax_5(self):
        expression = "pow(pow(abs(,5)))"
        self.helper(expression, False)

    def test_invalid_syntax_6(self):
        expression = "abs()"
        self.helper(expression, False)

    def test_invalid_syntax_7(self):
        expression = "pow(1,2,3)"
        self.helper(expression, False)

    def test_invalid_syntax_8(self):
        expression = "pow(1,pow(2,abs(,)))"
        self.helper(expression, False)


if __name__ == '__main__':
    unittest.main()
