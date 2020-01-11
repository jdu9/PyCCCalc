from PyQt5.QtWidgets import QMainWindow
from pycccalc.MainWindow import Ui_MainWindow

import re
import pyperclip


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.buttons.buttonClicked.connect(self.handle_buttons)
        self.push_copy.clicked.connect(self.copy_to_clipboard)
        self.expression.textChanged.connect(
            lambda: self.expression_color('000000')
        )

    def copy_to_clipboard(self):
        to_copy = self.result.text()
        pyperclip.copy(to_copy.replace('~', '', 1))

    def handle_buttons(self, button):
        """Handle all normal buttons."""
        value = button.text()
        if value != '':
            if value in '1234567890+-*/.()':
                self.add_to_expression(
                    value
                )
            elif value == 'C':
                self.clear()
            elif value == 'Del':
                self.delete_last()

    def add_to_expression(self, char):
        """On button click, add character to expression field."""
        text = self.expression.text()
        pos = self.expression.cursorPosition()
        text = text[:pos] + char + text[pos + 1:]
        self.set_expression(text)

    def expression_color(self, color):
        """Change color of expression field."""
        if re.search('^[0-9A-Fa-f]{6}$', color) is not None:
            self.expression.setStyleSheet('color:#{};'.format(color))
            return
        raise Exception("Invalid color code!")

    def clear(self):
        """Clear expression field."""
        self.result.setText("0")
        self.expression.setText("")

    def delete_last(self):
        """Delete character on cursor or last character."""
        text = self.expression.text()
        pos = self.expression.cursorPosition()
        if pos == len(text):
            text = text[:-1]
        else:
            text = text[:pos] + text[pos + 1:]
        self.expression.setText(text)

    def set_expression(self, string):
        self.expression.setText(string)

    def set_result(self, string):
        self.result.setText(string)

    def get_expression(self):
        return self.expression.text()

    def get_result(self):
        return self.expression.text()
