from typing import List

from entities.argument import Cell
from entities.content import Content, Text, Operand
from entities.operator import Operator


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

    def get_formula_result(self) -> float:
        """
        @summary: Returns the result of a formula.
        @return: Result of the formula as a float.
        @raises TokenizationFormatInFormulaException: Raises if the format of any token is incorrect.
        @raises SyntaxErrorInFormulaException: Raises if there is a syntax error in the formula.
        @raises CircularDependencyException: Raises if there is a circular dependency in the formula.
        @raises ExpressionPostfixEvaluationException: Raises if there is an error evaluating the postfix expression in the formula.
        """

    # Implementing get_value function from superclass and overwriting it to get_formula_result
    get_value = get_formula_result
