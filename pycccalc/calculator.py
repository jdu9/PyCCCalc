class Calculator:
    """Logic for pycccalc. Written without any dependencies in mind.

    Attributes:
        result: Numeric representation of the result set by evaluate().
        output: String representation of the result set by evaluate().
        decimals: Decimals for output if result is a floating point number.
        variables: A dict of variables to be interpreted by the calculator.
        functions: A dict of functions to be interpreted by the calculator.
        success: Indicate whether the last input resulted in a success.
    """

    class CharWalker:
        """Wrapper class eating all the characters."""

        def __init__(self, chars):
            self.chars = chars.replace(' ', '')
            if len(self.chars) == 0:
                raise Exception("Empty expression!")

        def char(self):
            return self.chars[:1]

        def next(self):
            self.chars = self.chars[1:]

    def __init__(self, decimals=11, variables={}, functions={}):
        self.__reset()
        self.decimals = decimals
        self.variables = variables
        self.functions = functions

    def __reset(self, input_=''):
        """Set/Reset all fields for new calculation."""

        # End result.
        self.result = 0

        # Output for UI.
        self.output = ''

        self.success = True

    def evaluate(self, input_):
        """Evaluate input, set output field, return self."""
        self.__reset(input_)
        if len(input_) == 0:
            self.success = False
            self.output = 'Empty expression!'
        else:
            try:
                # Call Sum(Product(Group(Number|Variable|Function))).
                self.result = self.process_start(
                    self.CharWalker(input_)
                )
                if type(self.result) is float:
                    # Show possible imprecision if result is a fp number.
                    self.output = '~'
                    # Remove trailing zeros
                    # and a possible decimal seperator at the end.
                    self.output += str(
                        round(self.result, self.decimals)
                    )
                    if 'e' not in self.output:
                        self.output = self.output.rstrip("0").rstrip(".")
                else:
                    self.output = str(self.result)
                self.success = True
            except Exception as e:
                self.success = False
                self.output = str(e)
        return self

    def process_signs(self, cwalker):
        """Process all signs and return final sign."""
        sign = 1
        while len(cwalker.chars) > 0:
            if cwalker.char() == '-':
                sign *= -1
            elif cwalker.char() != '+':
                break
            cwalker.next()
        return sign

    def process_start(self, cwalker):
        """Catch any surplus characters."""
        result = self.process_sum(cwalker)
        if len(cwalker.chars) > 0:
            raise Exception("Some characters are lost!")
        return result

    def process_sum(self, cwalker):
        """Add or substract all products."""
        partial_result = self.process_product(cwalker)

        while len(cwalker.chars) > 0:
            if cwalker.char() == '+':
                cwalker.next()
                partial_result += self.process_product(cwalker)
            elif cwalker.char() == '-':
                cwalker.next()
                partial_result -= self.process_product(cwalker)
            else:
                break

        return partial_result

    def process_product(self, cwalker):
        """Use multiplication or division for all terms."""
        partial_result = self.process_term(cwalker)

        while len(cwalker.chars) > 0:
            if cwalker.char() == '*':
                cwalker.next()
                partial_result *= self.process_term(cwalker)
            elif cwalker.char() == '/':
                cwalker.next()
                tmp_value = self.process_term(cwalker)
                try:
                    partial_result /= tmp_value
                except ZeroDivisionError:
                    raise ZeroDivisionError("Division by zero!")
            else:
                break

        return partial_result

    def process_term(self, cwalker):
        """Do brackets."""
        sign = self.process_signs(cwalker)
        word = self.process_word(cwalker)

        if word is None:
            if cwalker.char() == '(':
                cwalker.next()
                if cwalker.char() == ')':
                    raise Exception("Brackets are empty!")
                tmp = self.process_sum(cwalker) * sign
                if cwalker.char() != ')':
                    raise Exception("Missing bracket!")
                cwalker.next()
                return tmp
            return self.process_number(cwalker) * sign
        else:
            return word

    def process_word(self, cwalker):
        """Either process word as function or as variable."""
        word = ''

        while len(cwalker.chars) > 0:
            if (cwalker.char().isalpha() or
               len(word) > 0 and cwalker.char().isdigit()):
                word += cwalker.char()
            else:
                break
            cwalker.next()

        if word != '':
            if word in self.functions.keys():
                return self.process_function(word, cwalker)
            if word in self.variables.keys():
                return self.variables[word]
            else:
                raise Exception("Unknown variable or function!")

        return None

    def process_function(self, fun, cwalker):
        """Process all arguments (by calling sum on them)
           and return result of specified function."""

        if cwalker.char() != '(':
            return None

        cwalker.next()

        arguments = []
        argument = ''

        level = 0
        while len(cwalker.chars) > 0:
            if cwalker.char() == '(':
                level = level + 1
            elif cwalker.char() == ')':
                level = level - 1
                if level < 0:
                    arguments.append(self.CharWalker(argument))
                    cwalker.next()
                    break
            elif level == 0 and cwalker.char() == ',':
                arguments.append(self.CharWalker(argument))
                argument = ''
                cwalker.next()
                continue
            argument += cwalker.char()
            cwalker.next()

        args = list(map(self.process_sum, arguments))
        return self.functions[fun](*args)

    def process_number(self, cwalker):
        """Return the next characters as float or int."""
        tmp_str = ''

        while len(cwalker.chars) > 0:
            if cwalker.char().isdigit():
                tmp_str += cwalker.char()
            elif cwalker.char() == '.':
                if '.' in tmp_str:
                    raise Exception("Invalid number!")
                tmp_str += '.'
            elif cwalker.char() not in '()+-*/':
                raise Exception("Some characters are lost!")
            else:
                break
            cwalker.next()

        try:
            if '.' in tmp_str:
                tmp_result = float(tmp_str)
            else:
                tmp_result = int(tmp_str)
        except ValueError:
            raise ValueError("Cannot convert number!")

        return tmp_result
