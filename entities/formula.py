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
        print(f"Text value: {text_value}")

        for match in pattern.finditer(text_value):
            identifier, number, _, operator = match.groups()
            if identifier and identifier.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                print(identifier)  # -> Not entering with AVERAGE
                list_of_tokens.append(("function", identifier.upper()))
            elif number:
                list_of_tokens.append(("number", number))
            elif operator:
                list_of_tokens.append(("operator", operator))
        print(f"List of tokens: {list_of_tokens}")
        return list_of_tokens

    def generate_postfix_expression(self) -> List[Union[str, float]]:
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

        for token_type, value in tokens:
            print(f"Token: {token_type, value}, Stack: {stack}")

            if token_type == "number":
                output.append(float(value))
            elif token_type == "function":
                stack.append(value)
            elif token_type == "operator" and value == "(":
                stack.append(value)
            elif token_type == "operator" and value == ")":
                while stack and stack[-1] != "(":
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
            elif isinstance(token, str):
                if token.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                    function_name = token.upper()
                    function_class = {
                        "SUM": SumFunction,
                        "MAX": MaxFunction,
                        "MIN": MinFunction,
                        "AVERAGE": AverageFunction,
                    }[function_name]
                    num_operands = function_class.get_num_operands()

                    # Pop the specified number of operands from the stack
                    operands = [stack.pop() for _ in range(num_operands)]

                    # If the function allows multiple arguments separated by semicolons,
                    # split the arguments and push each one onto the stack
                    if num_operands == 0:
                        operands = stack[::-1]
                        stack = []

                    # Reverse order for proper evaluation
                    operands.reverse()

                    # Instantiate function instance and push result back
                    function_instance = function_class(operands=operands)
                    result = function_instance.get_result(*operands)
                    stack.append(result)
            else:
                raise ValueError(f"Unexpected token: {token}")

        return stack[0] if stack else None

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
