from abc import ABC, abstractmethod
from typing import List
from .content import Operand, Argument, Cell, CellRange


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

    @classmethod
    def get_num_operands(cls) -> int:
        if hasattr(cls, "operands"):
            return len(cls.operands)
        return 0


class SumFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        return sum(
            float(arg) if isinstance(arg, (Cell, CellRange)) else arg for arg in args
        )


class MinFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        return min(
            float(arg) if isinstance(arg, (Cell, CellRange)) else arg for arg in args
        )


class MaxFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        return max(
            float(arg) if isinstance(arg, (Cell, CellRange)) else arg for arg in args
        )


class AverageFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, *args: Argument) -> float:
        args_values = [
            float(arg) if isinstance(arg, (Cell, CellRange)) else arg for arg in args
        ]

        # Descomentar la siguiente línea si se desea manejar el caso de AVERAGE sin argumentos
        # if not args_values:
        #     raise ValueError("AVERAGE function requires at least one argument")

        return sum(args_values) / len(args_values)
