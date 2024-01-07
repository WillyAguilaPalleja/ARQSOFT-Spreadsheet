from abc import ABC, abstractmethod
from typing import List
from .argument import Argument, Cell, CellRange
from .content import Operand


class FunctionABC(ABC):
    @abstractmethod
    def get_result(*args: Argument) -> float:
        pass

    @classmethod
    @abstractmethod
    def get_num_operands(cls) -> int:
        pass


class Function(FunctionABC, Argument):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__()
        self.operands = operands

    def get_result(*args: Argument) -> float:
        pass

    @classmethod
    def get_num_operands(cls) -> int:
        return len(cls.__annotations__["operands"].__args__)


class SumFunction(Function):
    def __init__(self, *operands: Operand) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        return sum(
            float(arg.get_value_as_number())
            if isinstance(arg, (Cell, CellRange))
            else arg.get_value_as_number()
            for arg in args
        )

    @classmethod
    def get_num_operands(cls) -> int:
        return len(cls.__annotations__["operands"].__args__)


class MinFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        return min(
            float(arg) if isinstance(arg, (Cell, CellRange)) else arg for arg in args
        )

    @classmethod
    def get_num_operands(cls) -> int:
        return len(cls.__annotations__["operands"].__args__)


class MaxFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        return max(
            float(arg) if isinstance(arg, (Cell, CellRange)) else arg for arg in args
        )

    @classmethod
    def get_num_operands(cls) -> int:
        return len(cls.__annotations__["operands"].__args__)


class AverageFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        args_values = [
            float(arg) if isinstance(arg, (Cell, CellRange)) else arg for arg in args
        ]
        return sum(args_values) / len(args_values)

    @classmethod
    def get_num_operands(cls) -> int:
        return len(cls.__annotations__["operands"].__args__)
