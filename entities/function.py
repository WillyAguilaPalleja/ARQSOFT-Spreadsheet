from abc import ABC, abstractmethod
from typing import List
from .content import Operand, Argument, Cell, CellRange, Number


def flatten(list_to_flatten: List) -> List:
    result = []
    for item in list_to_flatten:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


class FunctionABC(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_result(self, arguments: Argument) -> float:
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
        arguments_flattened = flatten(arguments)
        return (
            sum(
                float(arg.content.get_value_as_number())
                if isinstance(arg, (Cell, CellRange))
                else float(arg)
                for arg in arguments_flattened
            )
            if arguments_flattened
            else 0
        )


class MinFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, arguments: List[Number]) -> float:
        arguments_flattened = flatten(arguments)
        return (
            min(
                float(arg.content.get_value_as_number())
                if isinstance(arg, (Cell, CellRange))
                else float(arg)
                for arg in arguments_flattened
            )
            if arguments_flattened
            else 0
        )


class MaxFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, arguments: List[Number]) -> float:
        arguments_flattened = flatten(arguments)
        return (
            max(
                float(arg.content.get_value_as_number())
                if isinstance(arg, (Cell, CellRange))
                else float(arg)
                for arg in arguments_flattened
            )
            if arguments_flattened
            else 0
        )


class AverageFunction(Function):
    def __init__(self, operands: List[Operand]) -> None:
        super().__init__(operands=operands)

    def get_result(self, arguments: List[Number]) -> float:
        arguments_flattened = flatten(arguments)
        args_values = [
            float(arg.content.get_value_as_number())
            if isinstance(arg, (Cell, CellRange))
            else float(arg)
            for arg in arguments
        ]

        return sum(args_values) / len(args_values) if arguments_flattened else 0
