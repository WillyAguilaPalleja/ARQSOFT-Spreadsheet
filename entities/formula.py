from abc import ABC, abstractmethod
from typing import List












class Operand(ABC):
    def __init__(self) -> None:
        super().__init__()





class Number(Operand):
    def __init__(self, number_value: float) -> None:
        self.number_value = number_value

    def get_number_value(self) -> float:
        return self.number_value


class Text:
    def __init__(self, text_value: str) -> None:
        self.text_value = text_value

    def get_text_value(self) -> str:
        return self.text_value


class Content(ABC):
    def __init__(self, value: Number | Text) -> None:
        super().__init__()
        self.value = value

    @abstractmethod
    def get_value(self) -> Number | Text:
        pass


class NumericalContent(Content):
    def __init__(self, value: Number) -> None:
        super().__init__(value=value)

    def get_value(self) -> Number:
        """
        @summary: Returns the numerical value of the cell.
        @return: Numerical value as a float
        """
        return self.value

    def get_text_from_number(self) -> Text:
        """
        @summary: Returns the textual representation of the numerical value of
        the cell.
        @return: Textual representation of the numerical value of the cell.
        """
        return Text(text_value=str(self.value.get_number_value()))


class TextualContent(Content):
    def __init__(self, value: Text) -> None:
        super().__init__(value=value)

    def get_value(self) -> Text:
        """
        @summary: Returns the textual value of the cell.
        @return: Textual value as a string
        """
        return self.value

    def get_number_from_text(self) -> Number:
        """
        @summary: Returns the numerical representation of the textual value
        of the cell. If the cell is empty, returns a 0.0.
        @return: Textual representation of the numerical value of the cell.
        @raises NumericalRepresentationException: Raises if the value can not be converted to float (e.g. the value "Hello world").
        """
        return Number(number_value=float(self.value.get_text_value()))


class Operator(ABC):
    def __init__(self, operator: str) -> None:
        super().__init__()
        self.operator = operator

    @abstractmethod
    def get_operator(self) -> str:
        pass


class SumOperator(Operator):
    def __init__(self) -> None:
        super().__init__(operator="+")

    def get_operator(self) -> str:
        return self.operator


class SubstractionOperator(Operator):
    def __init__(self) -> None:
        super().__init__(operator="-")

    def get_operator(self) -> str:
        return self.operator


class MultiplyOperator(Operator):
    def __init__(self) -> None:
        super().__init__(operator="*")

    def get_operator(self) -> str:
        return self.operator


class DivisionOperator(Operator):
    def __init__(self) -> None:
        super().__init__(operator="/")

    def get_operator(self) -> str:
        return self.operator


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


if __name__ == "__main__":
    print(TextualContent(Text(text_value="Hello world")).value.get_text_value())
