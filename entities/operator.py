from abc import ABC, abstractmethod


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
