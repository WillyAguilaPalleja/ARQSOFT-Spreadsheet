from typing import Optional


class BadCommandException(Exception):
    """
    @summary: Exception raised when the command the user has input is not valid.
    """

    def __init__(
        self, message: Optional[str] = "The command input is not valid"
    ) -> None:
        self.message = message


class SpreadsheetLocationException(Exception):
    """
    @summary: Exception raised when any spreadsheet was found in path_name or the file did not exist.
    """

    def __init__(self, message: Optional[str] = "The spreadsheet location is not valid") -> None:
        self.message = message


class NoCellException(Exception):
    """
    @summary: Exception raised when the cell does not exist.
    """

    def __init__(self) -> None:
        self.message = "The cell with the given coordinates does not exist"


class NumericalRepresentationException(Exception):
    """
    @summary: Exception raised when the value of the cell does not have a valid numerical representation.
    """

    def __init__(self) -> None:
        self.message = (
            "The value of the cell does not have a valid numerical representation"
        )


class TokenizationFormatInFormulaException(Exception):
    """
    @summary: Exception raised when the format of any token of the formula is not valid.
    """

    def __init__(self) -> None:
        self.message = "The format of the formula is not valid"


class SyntaxErrorInFormulaException(Exception):
    """
    @summary: Exception raised when the formula has a syntax error.
    """

    def __init__(self) -> None:
        self.message = "The formula has a syntax error"


class CircularDependencyException(Exception):
    """
    @summary: Exception raised when the formula has a circular dependency.
    """

    def __init__(self) -> None:
        self.message = "The formula has a circular dependency"


class ExpressionPostfixEvaluationException(Exception):
    """
    @summary: Exception raised when the expression cannot be evaluated.
    """

    def __init__(self) -> None:
        self.message = "The expression cannot be evaluated"
