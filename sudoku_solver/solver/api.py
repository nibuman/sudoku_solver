from abc import abstractmethod, ABC
from typing import Callable

SudokuBoard = str


class ABCSolver(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def solve_sudoku(
        self,
        board: str,
        completed_board_validator: Callable[[SudokuBoard], bool],
        max_solutions: int,
    ) -> list[SudokuBoard]:
        pass
