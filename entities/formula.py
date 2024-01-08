from typing import List, Tuple, Any, Union
import re

from .content import Content, Text, Operand, Cell, Number
from .function import SumFunction, MinFunction, AverageFunction, MaxFunction, Function
from .operator import Operator


class Formula(Content):
    def __init__(
        self,
        formula_content: Text,
        spreadsheet_cells: List[Cell],
        operators_in_formula: List[Operator],
        operands_in_formula: List[Operand],
    ) -> None:
        super().__init__(value=formula_content)
        self.spreadsheet_cells = spreadsheet_cells
        self.operators_in_formula = operators_in_formula
        self.operands_in_formula = operands_in_formula
        self.formula_result = None

    def __str__(self) -> str:
        return str(Number(number_value=self.get_formula_result()))

    def replace_cell_reference(self, match: re.Match) -> str:
        cell_id = match.group(0).upper()
        print(f"Cell id: {cell_id}, type: {type(cell_id)}")
        for cell in self.spreadsheet_cells:
            if cell.cell_id == cell_id:
                print(f"Cell content: {cell.content}")
                if isinstance(cell.content, Formula):
                    return str(cell.content.get_formula_result() if cell.content.get_formula_result() else 0.0)
                elif isinstance(cell.content, Number):
                    return str(cell.content.get_number_value())
                elif isinstance(cell.content, Text):
                    return cell.content.get_text_value()

    def replace_cells_reference_in_formula(self, text_value: str) -> str:
        pattern = re.compile(r"[A-Za-z][A-Za-z0-9]*[0-9]*")
        while re.search(pattern, text_value):
            text_value = re.sub(pattern=pattern, repl=self.replace_cell_reference, string=text_value)
        return text_value

    def replace_numbers_in_functions(self, text_value: str) -> str:
        pattern = re.compile(r"([A-Za-z][A-Za-z0-9;]*)\(([^)]*)\)")

        def replace_argument(arg: str) -> str:
            return self.replace_cell_reference(arg.strip()) \
                if isinstance(arg, str) and re.match(r"^[A-Za-z](?:[1-9]|[1-9][0-9]|100)$", arg.strip()) \
                else arg

        def replace_numbers(match: re.Match) -> str:
            function_name = match.group(1)
            function_arguments = match.group(2).split(';')

            function_arguments = [replace_argument(arg) for arg in function_arguments]
            function_arguments = [Number(number_value=float(eval(arg))) for arg in function_arguments]

            print(f"Function arguments: {[argument.get_number_value() for argument in function_arguments]}")
            print(f"Function name: {function_name}")

            function_result = float(self.get_function_instance(function_name.upper()).get_result(function_arguments))
            return str(function_result)

        while re.search(pattern, text_value):
            text_value = re.sub(pattern=pattern, repl=replace_numbers, string=text_value)

        return text_value

    def tokenize_formula(self) -> List[Tuple[str, str, str]]:
        list_of_tokens = []
        pattern = re.compile(
            r"\s*([A-Za-z][A-Za-z0-9;]*)|(\d+(\.\d*)?)|([+\-*/();])\s*"
        )

        text_value = self.value.get_text_value()
        text_value = text_value[1:]

        #text_value = self.replace_cells_reference_in_formula(text_value)
        print(f"Text value: {text_value}")

        # Replace numbers inside functions recursively
        text_value = self.replace_numbers_in_functions(text_value)
        print(f"Text value: {text_value}")
        text_value = self.replace_cells_reference_in_formula(text_value)
        print(f"Text value: {text_value}")

        for match in pattern.finditer(text_value):
            identifier, number, _, operator = match.groups()
            if identifier and identifier.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                list_of_tokens.append(("function", identifier.upper(), '0'))
            elif number:
                list_of_tokens.append(("number", number, '0'))
            elif operator:
                list_of_tokens.append(("operator", operator, '0'))

        print(f"List of tokens: {list_of_tokens}")
        return list_of_tokens

    def extract_function_content(self, text_value: str) -> str:
        # Implement logic to extract the content of the function
        # You can use regular expressions or any other method
        # Here, I'm providing a simple example assuming arguments are separated by ';'
        start_index = text_value.find("(")
        end_index = text_value.find(")")
        if start_index != -1 and end_index != -1:
            return text_value[start_index + 1:end_index]
        else:
            return "0"

    def generate_postfix_expression(self) -> List[Union[str, float, Tuple[str, str]]]:
        output = []
        stack = []

        def precedence(operator: str) -> int:
            if operator in {"*", "/"}:
                return 2
            elif operator in {"+", "-"}:
                return 1
            elif operator in {"SUM", "MAX", "MIN", "AVERAGE"}:
                return 3
            else:
                return 0

        tokens = self.tokenize_formula()
        print(f"Tokens: {tokens}")

        for token_type, value, function_content in tokens:
            if token_type == "number":
                output.append(float(value))
            elif token_type == "operator":
                while stack and precedence(stack[-1][1]) >= precedence(value):
                    output.append(stack.pop())
                stack.append(("operator", value))
            elif value == "(":
                stack.append(("operator", value))
            elif value == ")":
                while stack and stack[-1][1] != "(":
                    output.append(stack.pop())
                stack.pop()  # Pop "("

        while stack:
            output.append(stack.pop())

        return output

    def evaluate_postfix(self) -> Any:
        stack = []

        postfix_expression = self.generate_postfix_expression()
        print(f"Postfix expression: {postfix_expression}")

        for token in postfix_expression:
            if isinstance(token, float):
                stack.append(token)
            elif isinstance(token, str):
                self.handle_operator(token, stack)
            elif isinstance(token, tuple):
                type, operator = token
                self.handle_operator(operator, stack)

        return stack[0] if stack else None

    def parse_function_arguments(self, function_content: str) -> List[Number]:
        # Implement logic to parse function arguments
        # Here, I'm assuming arguments are separated by ';'
        argument_values = function_content.split(';')

        # Special case for MIN and MAX functions
        if argument_values and ',' in argument_values[0]:
            # Handle MIN and MAX with multiple arguments
            return [Number(number_value=float(arg)) for arg in argument_values[0].split(',')]
        else:
            # Handle other functions with a single list of arguments
            return [Number(number_value=float(value)) for value in argument_values]

    def handle_operator(self, operator: str, stack: List[Any]):
        if operator == '+':
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append(operand1 + operand2)
        elif operator == '-':
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append(operand1 - operand2)
        elif operator == '*':
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append(operand1 * operand2)
        elif operator == '/':
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append(operand1 / operand2)

    def get_function_instance(self, function_name: str) -> Function:
        function_class = {
            "SUM": SumFunction,
            "MAX": MaxFunction,
            "MIN": MinFunction,
            "AVERAGE": AverageFunction,
        }[function_name]
        return function_class(operands=[])

    def get_formula_result(self) -> float:
        """
        @summary: Returns the result of a formula.
        @return: Result of the formula as a float.
        @raises TokenizationFormatInFormulaException: Raises if the format of any token is incorrect.
        @raises SyntaxErrorInFormulaException: Raises if there is a syntax error in the formula.
        @raises CircularDependencyException: Raises if there is a circular dependency in the formula.
        @raises ExpressionPostfixEvaluationException: Raises if there is an error evaluating the postfix expression in the formula.
        """
        result = self.evaluate_postfix()
        self.formula_result = result
        print(f"Formula result: {result}")
        return result

    # Implementing get_value function from superclass and overwriting it to get_formula_result
    get_value_as_number = get_formula_result
    get_value_as_text = get_formula_result
