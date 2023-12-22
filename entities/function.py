from abc import ABC, abstractmethod
from typing import List

from argument import Argument, Cell, CellRange
from content import Operand


class Function(ABC, Argument):
    def __init__(self, operands: List[Operand], arguments: List[Argument]) -> None:
        super().__init__()
        self.operands = operands
        self.arguments = arguments

    @abstractmethod
    def get_result(self, *args: float | Cell | CellRange) -> float:
        """
        @summary: Returns the result of the function.
        @param argument1: First argument of the function, can be of type float, Cell or CellRange.
        If being of type Cell or CellRange, needs to have a correct numerical value or the numerical representation
        of the textual value.
        ...
        @param argumentN: Last argument of the function, can be of type float, Cell or CellRange.
        If being of type Cell or CellRange, needs to have a correct numerical value or the numerical representation
        of the textual value.
        @return: Result of the function as a float.
        @raises SyntaxErrorInFunctionException: Raises if there is a syntax error in the function.
        """
        pass


class SumFunction(Function):
    def __init__(self, operands: List[Operand], arguments: List[Argument]) -> None:
        super().__init__(operands=operands, arguments=arguments)

    def get_result(self, *args: float | Cell | CellRange) -> float:
        pass


class MinFunction(Function):
    def __init__(self, operands: List[Operand], arguments: List[Argument]) -> None:
        super().__init__(operands=operands, arguments=arguments)

    def get_result(self, *args: float | Cell | CellRange) -> float:
        pass


class MaxFunction(Function):
    def __init__(self, operands: List[Operand], arguments: List[Argument]) -> None:
        super().__init__(operands=operands, arguments=arguments)

    def get_result(self, *args: float | Cell | CellRange) -> float:
        pass


class AverageFunction(Function):
    def __init__(self, operands: List[Operand], arguments: List[Argument]) -> None:
        super().__init__(operands=operands, arguments=arguments)

    def get_result(self, *args: float | Cell | CellRange) -> float:
        pass
