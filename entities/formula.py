from typing import List, Tuple, Any, Union
import re

from .argument import Cell
from .content import Content, Text, Operand
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
        pattern = re.compile(r"\s*([A-Za-z][A-Za-z0-9]*)|(\d+(\.\d*)?)|([+\-*/()])\s*")

        for match in pattern.finditer(self.value.get_text_value()):
            identifier, number, _, operator = match.groups()

            if identifier and identifier.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                list_of_tokens.append(("function", identifier.upper()))
            elif number:
                list_of_tokens.append(("number", number))
            elif operator:
                list_of_tokens.append(("operator", operator))

        return list_of_tokens

    def generate_postfix_expression(self) -> List[Union[str, float]]:
        output = []
        stack = []

        def precedence(operator: str) -> int:
            """
            Determines the precedence of an operator.
            """
            if operator in {"*", "/"}:
                return 2
            elif operator in {"+", "-"}:
                return 1
            elif operator in {"SUM", "MAX", "MIN", "AVERAGE"}:
                return 3
            else:
                return 0

        pattern = re.compile(r"\s*([A-Za-z][A-Za-z0-9]*)|(\d+(\.\d*)?)|([+\-*/()])\s*")
        formula_content = (
            self.value.get_text_value()
        )  # Fetch the text content of the formula
        for match in pattern.finditer(
            formula_content
        ):  # Pass the formula content as a string
            identifier, number, _, operator = match.groups()

            if identifier and identifier.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                stack.append(identifier.upper())
            elif number:
                output.append(float(number))
            elif operator:
                while (
                    stack
                    and stack[-1] != "("
                    and precedence(operator) <= precedence(stack[-1])
                ):
                    output.append(stack.pop())
                stack.append(operator)
            elif match.group() == "(":
                stack.append("(")
            elif match.group() == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()  # Pop the '('

        while stack:
            output.append(stack.pop())

        return output

    def evaluate_postfix(self) -> Any:
        stack = []

        postfix_expression = self.generate_postfix_expression()

        for token in postfix_expression:
            print(f"Token: {token}, Stack: {stack}")
            if isinstance(token, (float, int)):
                # Number: push onto the stack
                stack.append(token)
            elif token.isalpha():
                # Identifier: handle as needed (e.g., fetch value from a spreadsheet)
                stack.append(token)
            elif token in ["+", "-", "*", "/"]:
                # Operator: pop operands, perform operation, and push result back
                operand2 = stack.pop()
                operand1 = stack.pop()

                if token == "+":
                    result = operand1 + operand2
                elif token == "-":
                    result = operand1 - operand2
                elif token == "*":
                    result = operand1 * operand2
                elif token == "/":
                    result = operand1 / operand2

                stack.append(result)
            elif isinstance(token, Function):
                # Function: pop operands, and push result back
                num_operands = token.get_num_operands()
                operands = [stack.pop() for _ in range(num_operands)]
                operands.reverse()  # Reverse order for proper evaluation
                result = token.get_result(*operands)
                stack.append(result)

        # The final result should be on the top of the stack
        print(f"Final Stack: {stack}")
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
