from PyQt5.QtWidgets import QApplication
from pycccalc.window import MainWindow
from pycccalc.calculator import Calculator

import math
import json
import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class Application(QApplication):

    def __init__(self, args):
        super().__init__(sys.argv)

        try:
            variables = json.loads(args.variables)
        except json.decoder.JSONDecodeError:
            variables = {}

        functions = {
            'abs': abs,
            'pow': math.pow,
            'floor': math.floor,
            'log': math.log,
            'sqrt': math.sqrt,
            'ceil': math.ceil,
            'exp': math.exp,
            'remainder': math.remainder,
            'sin': math.sin,
            'tanh': math.tanh,
            'cos': math.cos,
            'cosh': math.cosh
        }

        self.calculator = Calculator(
            decimals=args.decimals,
            variables=variables,
            functions=functions
        )

        self.window = MainWindow()
        self.window.push_result.clicked.connect(self.calc)
        self.window.expression.returnPressed.connect(self.calc)
        self.window.push_ac.clicked.connect(self.all_clear)
        self.window.show()

    def calc(self):
        """Connect window with Calculator output. """
        if self.calculator.evaluate(
            self.window.get_expression()
        ).success:
            self.window.expression_color("000000")
            self.window.set_result(self.calculator.output)
            self.window.expression.setToolTip("Expression")
        else:
            self.window.expression_color("FF0000")
            self.window.expression.setToolTip(self.calculator.output)

    def all_clear(self):
        """Clear expression, set result to zero and delete all variables"""
        self.calculator.variables = {}
        self.window.clear()


def run(args):
    """Run everything!"""
    qt_app = Application(args)
    return qt_app.exec_()
