from enum import Enum
from typing import List

from entities.argument import Cell


class AvailableCommandsEnum(str, Enum):
    RF = "RF"
    C = "C"
    E = "E"
    L = "L"
    S = "S"


class Spreadsheet:
    _instance = None

    def __init__(self) -> None:
        if not Spreadsheet._instance:
            Spreadsheet._instance = self
            self.controller = SpreadsheetFactory.create_spreadsheet_controller()
            self.list_of_cells = SpreadsheetFactory.create_list_of_cells()


class UserInterface:
    _instance = None

    def __init__(self) -> None:
        if not UserInterface._instance:
            UserInterface._instance = self
            self.controller = SpreadsheetFactory.create_spreadsheet_controller()

    def send_command(self) -> str:
        """
        @summary: Sends the command the user has input to the SpreadsheetController.
        @return: The command typed in by the user.
        """


class SpreadsheetController:
    _instance = None

    def __init__(self) -> None:
        if not SpreadsheetController._instance:
            SpreadsheetController._instance = self
            self.spreadsheet = Spreadsheet()
            self.user_interface = UserInterface()

    def read_command(self, command: str) -> Spreadsheet | None:
        """
        @summary: Reads the command sent by the UI and performs the action needed for this command.
        @param command: Command sent by the UI
        @return: None.
        @raise BadCommandException: Raises if the command the user has input is not valid.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name or the file did not exist.
        """

    def create_spreadsheet(self) -> Spreadsheet:
        """
        @summary: Creates a spreadsheet using the method create_spreadsheet from SpreadsheetCreation.
        @return: Spreadsheet.
        """

    def load_spreadsheet(self, path_name: str) -> Spreadsheet:
        """
        @summary: Loads a spreadsheet given its route using the method load_spreadsheet from SpreadsheetLoader.
        @param path_name: Path where the spreadsheet to be loaded is located.
        @return: Spreadsheet.
        """

    def save_spreadsheet(self, path_name: str) -> None:
        """
        @summary: Saves the spreadsheet in the route given using the method save_spreadsheet from SpreadsheetSaver.
        @param path_name: Path where the spreadsheet to be saved is located.
        @return: None.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name or the file did not exist.
        """

    def edit_cell(self, cell_coordinate: str, new_cell_content: str) -> None:
        """
        @summary: Edits the cell given its coordinates and places the new content given using the method edit_cell from CellEdition.
        @param cell_coordinate: Coordinate of the cell where to modify its content.
        @param new_cell_content: New content of the cell.
        @return: None

        """

    def exit(self) -> None:
        """
        @summary: Close the application.
        """


class SpreadsheetFactory:
    @staticmethod
    def create_spreadsheet_controller() -> SpreadsheetController:
        """
        @summary: Creates the SpreadsheetController to be used.
        @return: SpreadsheetController.
        """
        return SpreadsheetController()

    @staticmethod
    def create_list_of_cells() -> List[Cell]:
        """
        @summary: Creates a list of cells to be used by the Spreadsheet.
        @return: List of cells.
        """
