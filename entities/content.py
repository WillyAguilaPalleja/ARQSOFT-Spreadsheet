from abc import ABC, abstractmethod


class Operand(ABC):
    def __init__(self) -> None:
        super().__init__()


class Number(Operand):
    def __init__(self, number_value: float) -> None:
        super().__init__()
        self.number_value = number_value

    def get_number_value(self) -> float:
        return self.number_value


class Text:
    def __init__(self, text_value: str) -> None:
        self.text_value = text_value

    def get_text_value(self) -> str:
        return self.text_value


class Content(ABC):
    def __init__(self, value: Number | Text) -> None:
        super().__init__()
        self.value = value

    @abstractmethod
    def get_value_as_number(self) -> Number | Text:
        pass

    @abstractmethod
    def get_value_as_text(self) -> Number | Text:
        pass


class NumericalContent(Content):
    def __init__(self, value: Number) -> None:
        super().__init__(value=value)

    def __str__(self) -> str:
        return str(self.value.get_number_value())

    def get_value_as_number(self) -> Number:
        """
        @summary: Returns the numerical value of the cell.
        @return: Numerical value as a float
        """
        return self.value

    def get_value_as_text(self) -> Text:
        """
        @summary: Returns the textual representation of the numerical value of
        the cell.
        @return: Textual representation of the numerical value of the cell.
        """
        return Text(text_value=str(self.value.get_number_value()))


class TextualContent(Content):
    def __init__(self, value: Text) -> None:
        super().__init__(value=value)

    def __str__(self) -> str:
        return self.value.text_value

    def get_value_as_text(self) -> Text:
        """
        @summary: Returns the textual value of the cell.
        @return: Textual value as a string
        """
        return self.value

    def get_value_as_number(self) -> Number:
        """
        @summary: Returns the numerical representation of the textual value
        of the cell. If the cell is empty, returns a 0.0.
        @return: Textual representation of the numerical value of the cell.
        @raises NumericalRepresentationException: Raises if the value can not be converted to float (e.g. the value "Hello world").
        """
        return Number(number_value=float(self.value.get_text_value()))
