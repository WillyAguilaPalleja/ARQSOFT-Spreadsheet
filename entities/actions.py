from .spreadsheet import Spreadsheet


class SpreadsheetCreation:
    def create_spreadsheet(self) -> Spreadsheet:
        """
        @summary: Create a Spreadsheet from scratch
        @return: Spreadsheet
        """


class SpreadsheetLoader:
    def load_spreadsheet(self, path_name: str) -> Spreadsheet:
        """
        @summary: Loads a spreadsheet given its route.
        @param path_name: Path where the spreadsheet to be loaded is located.
        @return: Spreadsheet.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name.
        """


class SpreadsheetSaver:
    def save_spreadsheet(self, path_name: str) -> None:
        """
        @summary: Saves the spreadsheet in the route given.
        @param path_name: Path where the spreadsheet to be saved is located.
        @return: None.
        @raises SpreadsheetLocationException: Raises if a spreadsheet with the same path has been found.
        """


class CellEdition:
    def edit_cell(self, cell_coordinate: str, new_cell_content: str) -> None:
        """
        @summary: Edits the cell given its coordinates and places the new content given.
        @param cell_coordinate: Coordinate of the cell where to modify its content.
        @param new_cell_content: New content of the cell.
        @return: None
        @raises NoCellException: Raises if a cell with this cell coordinate does not exist.
        """
