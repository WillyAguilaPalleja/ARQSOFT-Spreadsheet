import os
import re
import time
from enum import Enum
from typing import List

from entities.content import (
    TextualContent,
    Text,
    Content,
    NumericalContent,
    Number,
    Cell,
)
from entities.formula import Formula
from exceptions.exceptions import (
    BadCommandException,
    SpreadsheetLocationException,
    CircularDependencyException,
    SyntaxErrorInFormulaException,
    TokenizationFormatInFormulaException,
    ExpressionPostfixEvaluationException,
    ValueErrorInFormulaException,
)
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

    def build_dependency_graph(self) -> None:
        # Build a directed acyclic graph (DAG) based on cell dependencies
        # You may need to adapt this based on your specific implementation
        for cell in self.list_of_cells:
            dependencies = self.find_dependencies(cell.content)
            self.dependency_graph[cell.cell_id] = dependencies

    def find_dependencies(self, content: Content) -> List[str]:
        # Implement logic to find dependencies for a given content
        # You may need to adapt this based on your specific implementation
        dependencies = []
        if isinstance(content, Formula):
            # Example: extract cell references from the formula
            dependencies = re.findall(
                r"[A-Za-z][A-Za-z0-9]*[0-9]*", content.value.get_text_value()
            )
        return dependencies

    def evaluate_spreadsheet(self) -> None:
        # Topologically sort the cells based on dependencies
        evaluation_order = self.topological_sort()

        # Evaluate cells in the determined order
        for cell_id in evaluation_order:
            cell = self.find_cell_by_id(cell_id)
            if cell and isinstance(cell.content, Formula):
                cell.content.get_formula_result()

    def topological_sort(self) -> List[str]:
        # Implement topological sorting algorithm
        # You may need to adapt this based on your specific implementation
        visited = set()
        order = []

        def visit(cell_id: str):
            if cell_id not in visited:
                visited.add(cell_id)
                for dependency in self.dependency_graph.get(cell_id, []):
                    visit(dependency)
                order.append(cell_id)

        for cell_id in self.dependency_graph.keys():
            visit(cell_id)

        return order

    def find_cell_by_id(self, cell_id: str) -> Cell | None:
        for cell in self.list_of_cells:
            if cell.cell_id == cell_id:
                return cell
        return None

    def display_spreadsheet(self, current_cell_id: str = None):
        beginning_of_line = "\033[1;32m|\033[0m"
        beginning_of_line_bold = "\033[1;32;1m|\033[0m"
        horizontal_line = "\033[1;34m" + "-" * (26 * 40) + "\033[0m"
        end_of_line = "\033[1;32m|\033[0m\n"
        cell_string = beginning_of_line + horizontal_line + end_of_line

        for row_index in range(1, 101):
            cell_string += beginning_of_line_bold
            for col_index in range(1, 27):
                cell_id = f"{chr(64 + col_index)}{row_index}"
                cell = self.find_cell_by_id(cell_id)

                if cell and cell.content:
                    content_str = str(cell.content)
                else:
                    content_str = ""

                if cell_id == current_cell_id:
                    cell_string += f"\033[1;37;45m {f'{cell_id}:'} \033[0m{beginning_of_line_bold}\033[1;37;45m{content_str:^38}\033[0m{beginning_of_line_bold}"
                else:
                    cell_string += f"{content_str:^38}{beginning_of_line_bold}"

            cell_string += (
                end_of_line + beginning_of_line + horizontal_line + end_of_line
            )

        print(cell_string)


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
                if read_command is False:
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
            self.spreadsheet: None | Spreadsheet = None
            self.user_interface: UserInterface = UserInterface()

    def read_command(self, command: str) -> Spreadsheet | bool | None:
        """
        @summary: Reads the command sent by the UI and performs the action needed for this command.
        @param command: Command sent by the UI
        @return: None.
        @raise BadCommandException: Raises if the command the user has input is not valid.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name or the file did not exist.
        """

        def read_command_from_a_file(path_name: str):
            try:
                with open(path_name, "r") as file:
                    for line in file:
                        self.read_command(line.strip())
            except FileNotFoundError:
                raise SpreadsheetLocationException(
                    message="The file in the route provided does not exist"
                )

        command_splitted = command.split(" ")
        try:
            match command_splitted[0].upper():
                case AvailableCommandsEnum.RF:
                    return read_command_from_a_file(path_name=command_splitted[1])
                case AvailableCommandsEnum.C:
                    return self.create_spreadsheet()
                case AvailableCommandsEnum.E:
                    self.edit_cell(
                        cell_coordinate=command_splitted[1],
                        new_cell_content=" ".join(command_splitted[2:]),
                    )
                    return self.spreadsheet.display_spreadsheet()
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
        except SyntaxErrorInFormulaException as e:
            print(e.message)
        except ValueErrorInFormulaException as e:
            print(e.message)
        except TokenizationFormatInFormulaException as e:
            print(e.message)
        except ExpressionPostfixEvaluationException as e:
            print(e.message)
        except CircularDependencyException as e:
            print(e.message)

    def create_spreadsheet(self) -> None:
        """
        @summary: Creates a spreadsheet using the method create_spreadsheet from SpreadsheetCreation.
        @return: None.
        """
        self.spreadsheet = Spreadsheet()
        self.spreadsheet.list_of_cells = SpreadsheetFactory.create_list_of_cells()
        self.spreadsheet.display_spreadsheet()

    def load_spreadsheet(self, path_name: str) -> Spreadsheet:
        spreadsheet = Spreadsheet()
        if path_name.split(".")[-1] != "s2v":
            raise SpreadsheetLocationException(
                message="The file in the route provided is not a .s2v file"
            )
        list_of_cells = [
            Cell(
                cell_id=f"{chr(65 + col_index)}{row_index + 1}",
                content=TextualContent(value=Text(text_value="")),
            )
            for row_index in range(100)
            for col_index in range(26)
        ]
        spreadsheet.list_of_cells = list_of_cells
        self.spreadsheet = spreadsheet

        with open(path_name, "r") as file:
            row_index = 0

            for line in file:
                line = line.strip()
                line_values = line.split(";")

                for col_index, cell_content in enumerate(line_values[:26]):
                    parsed_content = self.parse_s2v_content(cell_content, list_of_cells)

                    index = row_index * 26 + col_index
                    list_of_cells[index].content = parsed_content

                row_index += 1
                if row_index >= 100:
                    break

        for row in range(row_index, 100):
            for col_index in range(26):
                index = row * 26 + col_index
                list_of_cells[index].content = TextualContent(value=Text(text_value=""))

        spreadsheet.display_spreadsheet()
        return spreadsheet

    @staticmethod
    def parse_s2v_content(s2v_content: str, list_of_cells: List[Cell]) -> Content:
        s2v_content = s2v_content.strip()

        if s2v_content.startswith("="):
            return Formula(
                formula_content=Text(text_value=s2v_content.replace(",", ";")),
                spreadsheet_cells=list_of_cells,
                operators_in_formula=[],
                operands_in_formula=[],
            )
        elif s2v_content.replace(".", "", 1).isdigit():
            return NumericalContent(value=Number(number_value=float(s2v_content)))
        else:
            return TextualContent(value=Text(text_value=s2v_content))

    @staticmethod
    def remove_trailing_semicolons(row_list: List[str]):
        i = len(row_list) - 1
        while i >= 0 and row_list[i] == "":
            i -= 1
        return row_list[: i + 1]

    def save_spreadsheet(self, path_name: str) -> None:
        """
        @summary: Saves the spreadsheet in the route given using the method save_spreadsheet from SpreadsheetSaver.
        @param path_name: Path where the spreadsheet to be saved is located.
        @return: None.
        @raise SpreadsheetLocationException: Raises if any spreadsheet was found in path_name or the file did not exist.
        """
        if path_name.split(".")[-1] != "s2v":
            raise SpreadsheetLocationException(
                message="The file in the route provided is not a .s2v file"
            )
        if os.path.exists(path_name):
            raise SpreadsheetLocationException(
                message=f"A file with name {path_name} already exists, please pick another one."
            )
        elif not self.spreadsheet:
            raise SpreadsheetLocationException(
                message="You need to create or load a spreadsheet first"
            )

        with open(path_name, "w") as file:
            for row_index in range(100):
                row_string = ""

                for col_index in range(26):
                    index = row_index * 26 + col_index
                    cell = self.spreadsheet.list_of_cells[index]

                    if isinstance(cell.content, Formula):
                        if isinstance(cell.content.value, Text):
                            row_string += f"{cell.content.value.get_text_value().replace(';', ', ')};"
                        else:
                            row_string += f"{cell.content.value.get_number_value()};"

                    elif isinstance(cell.content, NumericalContent):
                        # Check if it's the first value in the row
                        if row_string == "":
                            row_string += f"{cell.content.value.get_number_value()}"
                        else:
                            row_string += f";{cell.content.value.get_number_value()}"

                    elif isinstance(cell.content, TextualContent):
                        text_value = f"{cell.content.value.get_text_value()}"
                        if text_value in ["0", "0.0", "None", ""]:
                            row_string += ";"
                        else:
                            row_string += f"{text_value};"

                # Remove trailing semicolons from the right
                row_list = row_string.split(";")
                row_list = self.remove_trailing_semicolons(row_list)
                row_string = ";".join(
                    value if value != "" else "" for value in row_list
                )

                if len(row_list) > 0:
                    file.write(f"{row_string}\n")
                else:
                    file.write("\n")

        # Close the file
        file.close()

    def edit_cell(self, cell_coordinate: str, new_cell_content: str) -> None:
        """
        @summary: Edits the cell given its coordinates and places the new content given using the method edit_cell from CellEdition.
        @param cell_coordinate: Coordinate of the cell where to modify its content.
        @param new_cell_content: New content of the cell.
        @return: None
        """
        if not self.spreadsheet:
            raise SpreadsheetLocationException(
                message="You need to load a spreadsheet first"
            )

        for cell in self.spreadsheet.list_of_cells:
            if cell.cell_id == cell_coordinate:
                if new_cell_content.strip()[0] == "=":
                    cell.content = Formula(
                        formula_content=Text(text_value=new_cell_content),
                        spreadsheet_cells=self.spreadsheet.list_of_cells,
                    )
                    for cell in self.spreadsheet.list_of_cells:
                        if isinstance(cell.content, Formula):
                            cell.content.get_formula_result()
                try:
                    new_cell_content_to_float = float(new_cell_content)
                    cell.content = NumericalContent(
                        value=Number(number_value=new_cell_content_to_float)
                    )

                except ValueError:
                    cell.content = TextualContent(Text(text_value=new_cell_content))

    @staticmethod
    def exit() -> bool:
        """
        @summary: Close the application.
        """
        print("Closing the application")
        time.sleep(1)
        return False


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
                col_label = chr(ord("A") + col_index)
                cell_id = f"{col_label}{row}"
                cell = Cell(
                    cell_id=cell_id, content=TextualContent(value=Text(text_value=""))
                )
                list_of_cells.append(cell)

        return list_of_cells
