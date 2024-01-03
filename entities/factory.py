from typing import List

from . import spreadsheet
from .argument import Cell
from .spreadsheet import SpreadsheetController, Spreadsheet


def create_spreadsheet(self):
    """
    @summary: Creates a spreadsheet using the method create_spreadsheet from SpreadsheetCreation.
    @return: Spreadsheet.
    """
    self.spreadsheet = Spreadsheet()


def edit_cell(self, cell_coordinate: str, new_cell_content: str) -> None:
    """
    @summary: Edits the cell given its coordinates and places the new content given using the method edit_cell from CellEdition.
    @param cell_coordinate: Coordinate of the cell where to modify its content.
    @param new_cell_content: New content of the cell.
    @return: None
    """
    # CHECK IF CELL EXISTS AND OTHER THINGS
    for cell in self.spreadsheet.list_of_cells:
        if cell.cell_id == cell_coordinate:
            # check formula content (no formula methods rn, priority high)
            cell.content = new_cell_content
            spreadsheet.SpreadsheetController.show_spreadsheet()
            return None
