from abc import abstractmethod, ABC
from typing import Callable


class ABCUI(ABC):
    def __init__(self, input_board: str | None, solver: Callable, validator) -> None:
        self.validator = validator
        self.input_board = input_board
        self.solver = solver

    @property
    def input_board(self):
        return self._board

    @input_board.setter
    def input_board(self, value):
        if not value:
            value = self._get_input()
        cleaned_board = self.validator.clean_string(value)
        if self.validator.validate_input_board(cleaned_board):
            self._board = cleaned_board
        else:
            raise ValueError

    @abstractmethod
    def run(self):
        pass

    def _get_input(self):
        pass
