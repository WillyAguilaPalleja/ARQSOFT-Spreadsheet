from typing import Optional


class BadCommandException(Exception):
    """
    @summary: Exception raised when the command the user has input is not valid.
    """

    def __init__(
        self, message: Optional[str] = "\nThe command input is not valid\n"
    ) -> None:
        self.message = message


class SpreadsheetLocationException(Exception):
    """
    @summary: Exception raised when any spreadsheet was found in path_name or the file did not exist.
    """

    def __init__(
        self, message: Optional[str] = "\nThe spreadsheet location is not valid\n"
    ) -> None:
        self.message = message


class NoCellException(Exception):
    """
    @summary: Exception raised when the cell does not exist.
    """

    def __init__(self) -> None:
        self.message = "\nThe cell with the given coordinates does not exist\n"


class NumericalRepresentationException(Exception):
    """
    @summary: Exception raised when the value of the cell does not have a valid numerical representation.
    """

    def __init__(self) -> None:
        self.message = (
            "\nThe value of the cell does not have a valid numerical representation\n"
        )


class TokenizationFormatInFormulaException(Exception):
    """
    @summary: Exception raised when the format of any token of the formula is not valid.
    """

    def __init__(self) -> None:
        self.message = "\nThe format of the formula is not valid\n"


class SyntaxErrorInFormulaException(Exception):
    """
    @summary: Exception raised when the formula has a syntax error.
    """

    def __init__(self) -> None:
        self.message = "\nThe formula has a syntax error\n"


class ValueErrorInFormulaException(Exception):
    """
    @summary: Exception raised when the formula has a syntax error.
    """

    def __init__(self) -> None:
        self.message = "\nOne of the values of the formula is not valid\n"


class CircularDependencyException(Exception):
    """
    @summary: Exception raised when the formula has a circular dependency.
    """

    def __init__(
        self,
        message: Optional[
            str
        ] = "\nThe formula can't be evaluated: it has a circular dependency\n",
    ) -> None:
        self.message = message


class ExpressionPostfixEvaluationException(Exception):
    """
    @summary: Exception raised when the expression cannot be evaluated.
    """

    def __init__(self) -> None:
        self.message = "The expression cannot be evaluated"
