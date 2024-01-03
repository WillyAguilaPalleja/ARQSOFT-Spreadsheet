import time
from enum import Enum
from typing import List

from entities import factory
from entities.argument import Cell
from exceptions import exceptions
from exceptions.exceptions import BadCommandException, SpreadsheetLocationException
from utils import help_message
from tabulate import tabulate


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
            except SpreadsheetLocationException as exception:
                print(exception.message)


class SpreadsheetController:
    _instance = None

    def __init__(self) -> None:
        if not SpreadsheetController._instance:
            SpreadsheetController._instance = self
            self.spreadsheet = Spreadsheet()
            self.user_interface = UserInterface()

    @staticmethod
    def show_spreadsheet():
        """
        @summary: Shows the spreadsheet to the user
        """
        headers = [''] + [chr(ord('A') + i) for i in range(len(SpreadsheetFactory.create_list_of_cells()))]
        rows = [[f"{i + 1}"] + [cell.content for cell in row] for i, row in enumerate(SpreadsheetFactory.create_list_of_cells())]

        print(tabulate(rows, headers, tablefmt="grid"))

    def read_command(self, command: str) -> Spreadsheet | None:
        """
        @summary: Reads the command sent by the UI and performs the action needed for this command.
        @param command: Command sent by the UI
        @return: None.
        @raise BadCommandException: Raises if the command the user has input is not valid.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name or the file did not exist.
        """

        # DOES NOT WORK WITH SEVERAL LINES
        def read_command_from_a_file(path_name: str):
            try:
                with open(path_name, "r") as file:
                    for line in file:
                        self.read_command(line.strip())
            except FileNotFoundError:
                raise SpreadsheetLocationException(message='The file in the route provided does not exist')

        command_splitted = command.split(" ")
        try:
            match command_splitted[0].upper():
                case AvailableCommandsEnum.RF:
                    read_command_from_a_file(path_name=command_splitted[1])
                case AvailableCommandsEnum.C:
                    return factory.create_spreadsheet()
                case AvailableCommandsEnum.E:
                    return factory.edit_cell(
                        cell_coordinate=command_splitted[1],
                        new_cell_content=command_splitted[2])
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

    def load_spreadsheet(self, path_name: str) -> Spreadsheet:
        """
            @summary: Loads a spreadsheet given its route.
            @param path_name: Path where the spreadsheet to be loaded is located.
            @return: Spreadsheet.
            @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name.
            """

        try:
            with open(path_name, 'r') as file:
                s2v_content = file.read()
                rows = s2v_content.split('\n')
                data = [row.split(';') for row in rows]
                self.spreadsheet = data
                # assign values to spreadsheet ( data -> cells/spreadsheet on return )

                return self.spreadsheet
        except Exception as e:
            raise exceptions.SpreadsheetLocationException(f"Error on locating the file")

    def save_spreadsheet(self, path_name: str) -> None:
        """
        @summary: Saves the spreadsheet in the route given using the method save_spreadsheet from SpreadsheetSaver.
        @param path_name: Path where the spreadsheet to be saved is located.
        @return: None.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name or the file did not exist.
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
        list_of_cells: List[Cell] = []
        columns = 26  # A to Z
        rows = 100

        for row in range(1, rows + 1):
            for col_index in range(columns):
                col_label = chr(ord('A') + col_index)
                cell_id = f'{col_label}{row}'
                cell = Cell(cell_id=cell_id)
                list_of_cells.append(cell)

        return list_of_cells


