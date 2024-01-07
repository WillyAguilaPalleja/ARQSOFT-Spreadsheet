from typing import List, Tuple, Any, Union
import re

from .content import Content, Text, Operand, Cell
from .function import SumFunction, MinFunction, AverageFunction, MaxFunction, Function
from .operator import Operator


class Formula(Content):
    def __init__(
        self,
        formula_content: Text,
        cells_in_formula: List[Cell],
        operators_in_formula: List[Operator],
        operands_in_formula: List[Operand],
    ) -> None:
        super().__init__(value=formula_content)
        self.cells_in_formula = cells_in_formula
        self.operators_in_formula = operators_in_formula
        self.operands_in_formula = operands_in_formula

    def tokenize_formula(self) -> List[Tuple[str | None | List[str | None], Any]]:
        list_of_tokens = []
        pattern = re.compile(
            r"\s*([A-Za-z][A-Za-z0-9;]*)|(\d+(\.\d*)?)|([+\-*/();])\s*"
        )

        text_value = self.value.get_text_value()

        for match in pattern.finditer(text_value):
            identifier, number, _, operator = match.groups()
            if identifier and identifier.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                # Found a function, extract its content
                function_content = self.extract_function_content(text_value)
                list_of_tokens.append(("function", identifier.upper(), function_content))
            elif number:
                list_of_tokens.append(("number", number, ''))
            elif operator:
                list_of_tokens.append(("operator", operator, ''))
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

        # Obtener la lista de tokens utilizando tokenize_formula
        tokens = self.tokenize_formula()

        for token_type, value, function_content in tokens:
            print(f"Token: {token_type, value, function_content}, Stack: {stack}, Output: {output}")

            if token_type == "number":
                output.append(float(value))
            elif token_type == "function":
                stack.append(("function", value, function_content))
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

        for token in postfix_expression:
            print(f"Token: {token}, Stack: {stack}")

            if isinstance(token, float):
                stack.append(token)
            elif isinstance(token, tuple):
                if token[0] == "function":
                    function_name, function_content = token[1], token[2]
                    function_instance = self.get_function_instance(function_name)
                    # Handle function call with its arguments
                    arguments = function_content.split(';')  # Adapt this based on your actual argument separation logic
                    # Evaluate the function with its arguments
                    result = function_instance.get_result(arguments)
                    stack.append(result)
                elif token[0] == "operator":
                    if token[1] == '+':
                        operand2 = stack.pop()
                        operand1 = stack.pop()
                        stack.append(operand1 + operand2)
                    elif token[1] == '-':
                        operand2 = stack.pop()
                        operand1 = stack.pop()
                        stack.append(operand1 - operand2)
                    elif token[1] == '*':
                        operand2 = stack.pop()
                        operand1 = stack.pop()
                        stack.append(operand1 * operand2)
                    elif token[1] == '/':
                        operand2 = stack.pop()
                        operand1 = stack.pop()
                        stack.append(operand1 / operand2)
            else:
                raise ValueError(f"Unexpected token: {token}")

        print(f"Final Stack: {stack}")

        return stack[0] if stack else None

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
        print(self.evaluate_postfix())

    # Implementing get_value function from superclass and overwriting it to get_formula_result
    get_value_as_number = get_formula_result
    get_value_as_text = get_formula_result
