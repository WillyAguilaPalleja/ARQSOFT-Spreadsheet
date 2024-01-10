from enum import Enum
from typing import List, Tuple, Any, Union
import re

from exceptions.exceptions import (
    CircularDependencyException,
    SyntaxErrorInFormulaException,
    TokenizationFormatInFormulaException,
    ExpressionPostfixEvaluationException,
    NumericalRepresentationException,
    ValueErrorInFormulaException,
)
from .content import (
    Content,
    Text,
    Operand,
    Cell,
    Number,
    NumericalContent,
    TextualContent,
    CellRange,
)
from .function import SumFunction, MinFunction, AverageFunction, MaxFunction, Function
from .operator import (
    Operator,
    SumOperator,
    SubstractionOperator,
    MultiplyOperator,
    DivisionOperator,
)


class OperatorEnum(str, Enum):
    ADD = SumOperator().operator
    SUBTRACT = SubstractionOperator().operator
    MULTIPLY = MultiplyOperator().operator
    DIVIDE = DivisionOperator().operator


class Formula(Content):
    def __init__(
        self,
        formula_content: Text,
        spreadsheet_cells: List[Cell],
    ) -> None:
        super().__init__(value=formula_content)
        self.spreadsheet_cells = spreadsheet_cells
        self.formula_result = None

    def __str__(self) -> str:
        return str(Number(number_value=self.get_formula_result()))

    def replace_cell_reference(self, match: re.Match) -> str:
        cell_id = match.group(0).upper()
        try:
            for cell in self.spreadsheet_cells:
                if cell.cell_id == cell_id:
                    if cell.content and isinstance(cell.content, Formula):
                        return str(cell.content.get_formula_result())
                    elif cell.content and isinstance(cell.content, NumericalContent):
                        return str(
                            cell.content.get_value_as_number().get_number_value()
                        )
                    elif cell.content and isinstance(cell.content, TextualContent):
                        return str(
                            cell.content.get_value_as_number().get_number_value()
                        )
                    else:
                        raise SyntaxErrorInFormulaException()
        except NumericalRepresentationException:
            raise ValueErrorInFormulaException()

    def replace_cells_reference_in_formula(self, text_value: str) -> str:
        pattern = re.compile(r"[A-Za-z][A-Za-z0-9]*[0-9]*")
        while re.search(pattern, text_value):
            text_value = re.sub(
                pattern=pattern, repl=self.replace_cell_reference, string=text_value
            )
        return text_value

    def replace_numbers_in_functions(self, text_value: str) -> str:
        pattern = re.compile(r"([A-Za-z][A-Za-z0-9;]*)\(([^)]*)\)")
        inside_function = [False]

        def get_cells_in_range(start_cell, end_cell):
            try:
                start_col, start_row = start_cell[0], int(start_cell[1:])
                end_col, end_row = end_cell[0], int(end_cell[1:])
            except ValueError:
                #  If the cell reference is not valid, raise an exception
                raise SyntaxErrorInFormulaException()

            cells_in_range = []
            for cell in self.spreadsheet_cells:
                if (
                    start_col <= cell.cell_id[0] <= end_col
                    and start_row <= int(cell.cell_id[1:]) <= end_row
                ):
                    cells_in_range.append(cell)

            return cells_in_range

        def replace_argument(arg: str) -> List[float] | str:
            if ":" in arg:
                start_cell, end_cell = arg.split(":")

                cell_range = get_cells_in_range(start_cell, end_cell)

                cell_range_obj = CellRange(cells_in_range=cell_range)

                values = []
                for cell in cell_range_obj.cells_in_range:
                    if isinstance(cell.content, Formula):
                        values.append(cell.content.get_formula_result())
                    elif isinstance(cell.content, TextualContent):
                        values.append(
                            cell.content.get_value_as_number().get_number_value()
                        )
                    elif isinstance(cell.content, NumericalContent):
                        values.append(
                            cell.content.get_value_as_number().get_number_value()
                        )
                    else:
                        values.append(0.0)
                return values

            else:  # Handle regular single cell reference
                return (
                    self.replace_cells_reference_in_formula(arg.strip())
                    if re.match(r"^[A-Za-z](?:[1-9]|[1-9][0-9]|100)$", arg.strip())
                    else arg
                    if arg != ""
                    else "0.0"
                )

        def replace_numbers(match: re.Match) -> str:
            function_name = match.group(1)
            function_arguments = match.group(2).split(";")

            function_arguments = [replace_argument(arg) for arg in function_arguments]
            function_arguments = [
                arg if arg != "" else Number(number_value=0.0)
                for arg in function_arguments
            ]

            function_result = self.get_function_instance(
                function_name.upper()
            ).get_result(function_arguments)

            inside_function[0] = False
            return str(function_result)

        for match in pattern.finditer(text_value):
            identifier, _ = match.groups()
            if identifier and identifier.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                inside_function[0] = True

        while re.search(pattern, text_value):
            text_value = re.sub(
                pattern=pattern, repl=replace_numbers, string=text_value
            )

        if ":" in text_value and not inside_function[0]:
            raise SyntaxErrorInFormulaException()

        return text_value

    def tokenize_formula(self) -> List[Tuple[str, str]]:
        list_of_tokens = []
        pattern = re.compile(
            r"\s*([A-Za-z][A-Za-z0-9;]*)|(\d+(\.\d*)?)|([+\-*/();])\s*"
        )

        text_value = self.value.get_text_value()
        text_value = text_value[1:]
        try:
            text_value = self.replace_numbers_in_functions(text_value)
        except KeyError:
            raise SyntaxErrorInFormulaException()
        except SyntaxErrorInFormulaException as e:
            raise e
        text_value = self.replace_cells_reference_in_formula(text_value)

        for match in pattern.finditer(text_value):
            identifier, number, _, operator = match.groups()
            if identifier and identifier.upper() in {"SUM", "MAX", "MIN", "AVERAGE"}:
                list_of_tokens.append(("function", identifier.upper()))
            elif number:
                list_of_tokens.append(("number", number))
            elif operator:
                if (
                    operator not in OperatorEnum.__members__.values()
                    and operator not in "()"
                ):
                    raise SyntaxErrorInFormulaException()
                list_of_tokens.append(("operator", operator))

        for token_type, value in list_of_tokens:
            if token_type not in ["number", "operator", "function"]:
                raise TokenizationFormatInFormulaException()

        return list_of_tokens

    def extract_function_content(self, text_value: str) -> str:
        start_index = text_value.find("(")
        end_index = text_value.find(")")
        if start_index != -1 and end_index != -1:
            return text_value[start_index + 1 : end_index]
        else:
            return "0"

    def generate_postfix_expression(self) -> List[Union[str, float, Tuple[str, str]]]:
        output = []
        stack = []

        def precedence(operator: str) -> int:
            if operator in {"*", "/"}:
                return 2
            elif operator in {"+", "-"}:
                return 1
            elif operator in {"SUM", "MAX", "MIN", "AVERAGE"}:
                return 3
            else:
                return 0

        tokens = self.tokenize_formula()

        for token_type, value in tokens:
            if token_type == "number":
                output.append(float(value))
            elif token_type == "operator":
                if value == "(":
                    stack.append(("operator", value))
                elif value == ")":
                    while stack and stack[-1][1] != "(":
                        output.append(stack.pop())
                    stack.pop()
                else:
                    while stack and precedence(stack[-1][1]) >= precedence(value):
                        output.append(stack.pop())
                    stack.append(("operator", value))

        while stack:
            output.append(stack.pop())

        return output

    def evaluate_postfix(self) -> NumericalContent | None:
        stack = []

        postfix_expression = self.generate_postfix_expression()
        try:
            for token in postfix_expression:
                if isinstance(token, float):
                    stack.append(token)
                elif isinstance(token, str):
                    self.handle_operator(token, stack)
                elif isinstance(token, tuple):
                    _type, operator = token
                    self.handle_operator(operator, stack)
        except Exception as e:
            print(e)
            raise ExpressionPostfixEvaluationException()

        return NumericalContent(value=Number(number_value=stack[0])) if stack else None

    def parse_function_arguments(self, function_content: str) -> List[Number]:
        argument_values = function_content.split(";")

        if argument_values and "," in argument_values[0]:
            return [
                Number(number_value=float(arg)) for arg in argument_values[0].split(",")
            ]
        else:
            return [Number(number_value=float(value)) for value in argument_values]

    def handle_operator(self, operator: str, stack: List[Any]):
        operand2 = stack.pop()
        operand1 = stack.pop()

        if operator == OperatorEnum.ADD:
            stack.append(operand1 + operand2)
        elif operator == OperatorEnum.SUBTRACT:
            stack.append(operand1 - operand2)
        elif operator == OperatorEnum.MULTIPLY:
            stack.append(operand1 * operand2)
        elif operator == OperatorEnum.DIVIDE:
            stack.append(operand1 / operand2)
        else:
            raise SyntaxErrorInFormulaException()

    def get_function_instance(self, function_name: str) -> Function:
        function_class = {
            "SUM": SumFunction,
            "MAX": MaxFunction,
            "MIN": MinFunction,
            "AVERAGE": AverageFunction,
        }[function_name]
        return function_class(operands=[])

    def get_formula_result(self) -> float:
        """
        @summary: Returns the result of a formula.
        @return: Result of the formula as a float.
        @raises TokenizationFormatInFormulaException: Raises if the format of any token is incorrect.
        @raises SyntaxErrorInFormulaException: Raises if there is a syntax error in the formula.
        @raises ValueErrorInFormulaException: Raises if there is a value error in the formula.
        @raises CircularDependencyException: Raises if there is a circular dependency in the formula.
        @raises ExpressionPostfixEvaluationException: Raises if there is an error evaluating the postfix expression in the formula.
        """
        try:
            result = self.evaluate_postfix()
            self.formula_result = result
            return result.get_value_as_number().get_number_value()
        except SyntaxErrorInFormulaException as e:
            raise e
        except TokenizationFormatInFormulaException as e:
            raise e
        except ExpressionPostfixEvaluationException as e:
            raise e
        except ValueErrorInFormulaException as e:
            raise e
        except RecursionError:
            raise CircularDependencyException()

    # Implementing get_value function from superclass and overwriting it to get_formula_result
    get_value_as_number = get_formula_result
    get_value_as_text = get_formula_result
