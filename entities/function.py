from abc import ABC, abstractmethod
from typing import List
from .content import Operand, Argument, Cell, CellRange, Number


class FunctionABC(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_result(self, *args: Argument) -> float:
        pass

    @classmethod
    @abstractmethod
    def get_num_operands(cls) -> int:
        pass


class Function(FunctionABC):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__()
        self.operands = operands

    @abstractmethod
    def get_result(self, arguments: List[Argument]) -> float:
        pass

    @classmethod
    def get_num_operands(cls) -> int:
        if hasattr(cls, "operands"):
            return len(cls.operands)
        return 0


class SumFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, arguments: List[Number]) -> float:
        return sum(
            float(arg) if isinstance(arg, (Cell, CellRange)) else float(arg.get_number_value()) for arg in arguments
        ) if arguments else 0


class MinFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, arguments: List[Number]) -> float:
        return min(
            float(arg) if isinstance(arg, (Cell, CellRange)) else float(arg.get_number_value()) for arg in arguments
        ) if arguments else 0


class MaxFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, arguments: List[Number]) -> float:
        return max(
            float(arg) if isinstance(arg, (Cell, CellRange)) else float(arg.get_number_value()) for arg in arguments
        ) if arguments else 0


class AverageFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, arguments: List[Number]) -> float:
        args_values = [
            float(arg) if isinstance(arg, (Cell, CellRange)) else float(arg.get_number_value()) for arg in arguments
        ]

        return sum(args_values) / len(args_values) if arguments else 0
