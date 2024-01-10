from entities.content import TextualContent, NumericalContent
from entities.formula import Formula
from entities.spreadsheet import SpreadsheetController
from marker.SpreadsheetMarkerForStudents.usecasesmarker.spreadsheet_controller_for_checker import \
    ISpreadsheetControllerForChecker


class MarkerController(ISpreadsheetControllerForChecker):

    def __init__(self):
        super().__init__()
        self.controller = SpreadsheetController()
        self.controller.read_command('c')

    def set_cell_content(self, coord, str_content):
        self.controller.edit_cell(cell_coordinate=coord, new_cell_content=str_content)

    def get_cell_content_as_float(self, coord) -> float:
        cell = self.controller.spreadsheet.find_cell_by_id(cell_id=coord)
        if isinstance(cell.content, TextualContent):
            return cell.content.get_value_as_number().get_number_value()
        elif isinstance(cell.content, NumericalContent):
            return cell.content.get_value_as_number().get_number_value()
        elif isinstance(cell.content, Formula):
            return cell.content.get_formula_result()

    def get_cell_content_as_string(self, coord) -> str:
        return self.controller.spreadsheet.find_cell_by_id(coord).content.get_value_as_text().get_text_value()

    def get_cell_formula_expression(self, coord):
        cell = self.controller.spreadsheet.find_cell_by_id(cell_id=coord)
        if isinstance(cell.content, TextualContent):
            return cell.content.get_value_as_number().get_number_value()
        elif isinstance(cell.content, NumericalContent):
            return cell.content.get_value_as_number().get_number_value()
        elif isinstance(cell.content, Formula):
            return cell.content.value.get_text_value()

    def save_spreadsheet_to_file(self, s_name_in_user_dir):
        return self.controller.save_spreadsheet(path_name=s_name_in_user_dir)

    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        return self.controller.load_spreadsheet(path_name=s_name_in_user_dir)


