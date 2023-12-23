from abc import ABC
from typing import List


class Argument(ABC):
    def __init__(self) -> None:
        super().__init__()


class Cell(Argument):
    def __init__(self, cell_id: str) -> None:
        super().__init__()
        self.cell_id = cell_id


class CellRange(Argument):
    def __init__(self, cells_in_range: List[Cell]) -> None:
        super().__init__()
        self.cells_in_range = cells_in_range
        self.first_cell_id = self.cells_in_range[0].cell_id
        self.last_cell_id = self.cells_in_range[-1].cell_id
