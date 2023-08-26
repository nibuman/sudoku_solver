from abc import abstractmethod, ABC
from typing import Callable

SudokuBoard = list[str]


class ABCSolver(ABC):
    @abstractmethod
    def __init__(self, board: str) -> None:
        pass

    @abstractmethod
    def solve_sudoku(
        self, max_solutions: int = 1, validator: Callable | None = None
    ) -> list[SudokuBoard]:
        pass
