import time
from enum import Enum
from typing import List

from entities.argument import Cell
from exceptions.exceptions import BadCommandException
from utils import help_message


class AvailableCommandsEnum(str, Enum):
    RF = "RF"
    C = "C"
    E = "E"
    L = "L"
    S = "S"
    Q = "Q"


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

    def send_command(self) -> None:
        """
        @summary: Sends the command the user has input to the SpreadsheetController.
        @return: The command typed in by the user.
        """
        user_wants_to_quit = False
        while not user_wants_to_quit:
            try:
                command = input("Enter a command: ")
                read_command = self.controller.read_command(command)
                if not read_command:
                    user_wants_to_quit = True
            except BadCommandException as exception:
                print(exception.message)
                print(help_message)


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
        command_splitted = command.split(" ")
        try:
            match command_splitted[0]:
                case AvailableCommandsEnum.RF:
                    # Read commands from a file
                    pass
                case AvailableCommandsEnum.C:
                    return self.create_spreadsheet()
                case AvailableCommandsEnum.E:
                    return self.edit_cell(
                        cell_coordinate=command_splitted[1],
                        new_cell_content=command_splitted[2],
                    )
                case AvailableCommandsEnum.L:
                    return self.load_spreadsheet(path_name=command_splitted[1])
                case AvailableCommandsEnum.S:
                    return self.save_spreadsheet(path_name=command_splitted[1])
                case AvailableCommandsEnum.Q:
                    return self.exit()
                case _:
                    raise BadCommandException()
        except IndexError:
            raise BadCommandException(
                message="The command input is not valid: not enough arguments were given"
            )

    def create_spreadsheet(self) -> Spreadsheet:
        """
        @summary: Creates a spreadsheet using the method create_spreadsheet from SpreadsheetCreation.
        @return: Spreadsheet.
        """
        pass

    def load_spreadsheet(self, path_name: str) -> Spreadsheet:
        """
        @summary: Loads a spreadsheet given its route using the method load_spreadsheet from SpreadsheetLoader.
        @param path_name: Path where the spreadsheet to be loaded is located.
        @return: Spreadsheet.
        """
        pass

    def save_spreadsheet(self, path_name: str) -> None:
        """
        @summary: Saves the spreadsheet in the route given using the method save_spreadsheet from SpreadsheetSaver.
        @param path_name: Path where the spreadsheet to be saved is located.
        @return: None.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name or the file did not exist.
        """
        pass

    def edit_cell(self, cell_coordinate: str, new_cell_content: str) -> None:
        """
        @summary: Edits the cell given its coordinates and places the new content given using the method edit_cell from CellEdition.
        @param cell_coordinate: Coordinate of the cell where to modify its content.
        @param new_cell_content: New content of the cell.
        @return: None
        """
        pass

    @staticmethod
    def exit() -> None:
        """
        @summary: Close the application.
        """
        print("Closing the application")
        time.sleep(1)
        return None


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
