from dataclasses import dataclass
from itertools import chain
from typing import Callable

SudokuBoard = list[str]
DigitsInPosition = set[str]
DigitsInPositions = list[DigitsInPosition]


class OutOfOptionsError(Exception):
    """No valid options for any digits in one or more positions of board"""


class BoardError(Exception):
    """Board is not a valid Sudoku board"""


@dataclass
class BoardPosition:
    possible_values: DigitsInPosition
    position: int = 0

    @property
    def options_count(self):
        return len(self.possible_values)


class SudokuSolver:
    __version__ = "8"
    DIGITS_1_TO_9 = {str(n) for n in range(1, 10)}
    DIGITS_0_TO_9 = {str(n) for n in range(0, 10)}
    ROW_INDICES = list(range(0, 81, 9))
    COL_INDICES = list(range(9))
    SQR_INDICES = [a + b for a in range(0, 81, 27) for b in range(0, 7, 3)]

    def __init__(self, board: str, max_solutions: int = 1) -> None:
        self.board = list(board)
        if not self.validate_input_board(board):
            raise BoardError("Input board was not valid")
        self.guess_stack: list[SudokuBoard] = []
        self.initialise_available_pos()
        self.difficulty_score = 0
        self.valid_solutions: list[SudokuBoard] = []

    def initialise_available_pos(self):
        self.available_pos_row = [[set() for _ in range(10)] for _ in range(9)]
        self.available_pos_col = [[set() for _ in range(10)] for _ in range(9)]
        self.available_pos_sqr = [[set() for _ in range(10)] for _ in range(9)]

    def get_rcs_alg2(self, position: int) -> list[DigitsInPositions]:
        """Returns the row, column and square for a particular cell for alg2"""
        r, c = self.get_index(position)
        s = self.get_sqr_index(r, c)
        return [
            self.available_pos_row[r],
            self.available_pos_col[c],
            self.available_pos_sqr[s],
        ]

    def reset_alg2(self):
        """Clears all the available positions used in alg2"""
        for rcs in chain(
            self.available_pos_row, self.available_pos_col, self.available_pos_sqr
        ):
            for position_set in rcs:
                position_set.clear()

    def update_alg2(self, position, available):
        alg2_rcs = self.get_rcs_alg2(position)
        for rcs in alg2_rcs:
            for num in available:
                rcs[int(num)].add(position)

    def get_sqr_index(self, row: int, col: int) -> int:
        """Identifies which 3x3 square (numbered 0-8) a given position is in:
        0 1 2
        3 4 5
        6 7 8
        e.g. position 0,3 will be square 0, 0,4 in square 1, and 8,7 in square 8.
        """
        return ((row // 3) * 3) + (col // 3)

    def get_index(self, position: int) -> tuple[int, int]:
        """Returns 2d coordinates of position in r,c format"""
        r = position // 9
        c = position % 9
        return (r, c)

    def get_row(self, position: int, sequence_type=set) -> DigitsInPosition:
        """Return set of numbers in row at given position"""
        r, _ = self.get_index(position)
        row_start = r * 9
        return sequence_type(self.board[row_start : row_start + 9])

    def get_col(self, position: int, sequence_type=set) -> DigitsInPosition:
        """Return set of numbers in column at given position"""
        _, c = self.get_index(position)
        return sequence_type(self.board[pos] for pos in range(c, 81, 9))

    def get_sqr(self, position: int, sequence_type=set) -> DigitsInPosition:
        """Return set of numbers in square at given position"""
        r, c = self.get_index(position)
        sq_start_pos = (r // 3) * 27 + (c // 3) * 3
        # offsets from starting position to visit every position in square
        offsets = (0, 1, 2, 9, 10, 11, 18, 19, 20)
        return sequence_type(self.board[sq_start_pos + offset] for offset in offsets)

    def get_not_available(self, position: int) -> DigitsInPosition:
        """Return set of numbers that are not available in given position"""
        row = self.get_row(position)
        col = self.get_col(position)
        sqr = self.get_sqr(position)
        return set.union(row, col, sqr)

    def get_available(self, position: int) -> DigitsInPosition:
        """Return set of numbers that are available in a given position"""
        not_available = self.get_not_available(position)
        return self.DIGITS_1_TO_9.difference(not_available)

    def validate_input_board(self, board: str) -> bool:
        if not all(
            [
                self.correct_number_of_digits(board),
                self.only_valid_digits(board, self.DIGITS_0_TO_9),
            ]
        ):
            return False

        return all(
            [
                self.digits_present_only_once(self.get_row, self.ROW_INDICES),  # Rows
                self.digits_present_only_once(
                    self.get_col, self.COL_INDICES
                ),  # Columns
                self.digits_present_only_once(
                    self.get_sqr, self.SQR_INDICES
                ),  # Squares
            ]
        )

    @staticmethod
    def only_valid_digits(board: str, valid_digits: set[str]) -> bool:
        return all(d in valid_digits for d in board)

    @staticmethod
    def correct_number_of_digits(board: str) -> bool:
        return len(board) == 81

    def all_digits_present(
        self, get_rcs: Callable[[int], set[str]], indices: list
    ) -> bool:
        """Check that all the digits and only the valid digit are present in
        each area (row, column or square). Accepts a function that returns the set
        of numbers in a given row/column/square and a sequence of the indices
        of each row/column/square to check"""
        return all(get_rcs(i) == self.DIGITS_1_TO_9 for i in indices)

    def digits_present_only_once(
        self,
        get_rcs: Callable,
        indices: list,
    ) -> bool:
        """Check that digits are present at most once in each area (row,
        column, or square)"""
        digits_present_only_once = []
        for i in indices:
            digits_without_zero = [d for d in get_rcs(i, list) if d != "0"]

            digits_present_only_once.append(
                sorted(digits_without_zero) == sorted(list(set(digits_without_zero)))
            )
        print(digits_present_only_once)
        return all(digits_present_only_once)

    def validate_complete_board(self) -> bool:
        """Checks whether sudoku board is valid by definition
        i.e. is there exactly one of each digit in each row, column and square"""
        return all(
            [
                self.correct_number_of_digits("".join(self.board)),
                self.all_digits_present(self.get_row, self.ROW_INDICES),  # Rows
                self.all_digits_present(self.get_col, self.COL_INDICES),  # Columns
                self.all_digits_present(self.get_sqr, self.SQR_INDICES),  # Squares
            ]
        )

    def get_options_for_free_positions(self) -> list[BoardPosition]:
        """Returns the digits that are possibilities in each free position"""
        return [
            BoardPosition(
                possible_values=self.get_available(position), position=position
            )
            for position, num_str in enumerate(self.board)
            if num_str == "0"
        ]

    def fill_free_positions(
        self, free_positions: list[BoardPosition]
    ) -> bool | list[BoardPosition]:
        """Goes through all the free positions and evaluates how many digits are
        possibilities in each. If any position has no options then there must be
        something wrong with board, if there's only 1 possibilty then fill that position
        with that digit and return True - otherwise return a list of all the positions
        with multiple options"""
        changed = False
        options = []
        for this_position in free_positions:
            match this_position:
                case BoardPosition(options_count=0):
                    raise OutOfOptionsError(
                        f"No options in position {this_position.position}"
                    )
                case BoardPosition(options_count=1):  # must be that number
                    self.board[
                        this_position.position
                    ] = this_position.possible_values.pop()
                    changed = True
                case _:
                    options.append(this_position)
                    self.update_alg2(
                        this_position.position, this_position.possible_values
                    )

        return changed or options

    def alg2(self) -> bool:
        """run the second algorithm - each row, col, sq must have 1 of all 9 numbers"""
        changed = False
        for rcs in chain(
            self.available_pos_row, self.available_pos_col, self.available_pos_sqr
        ):
            for number, available_pos in enumerate(rcs):
                if len(available_pos) == 1:
                    position = available_pos.pop()
                    self.board[position] = str(number)
                    changed = True
        return changed

    def generate_test_board(self, position: int, number: str) -> SudokuBoard:
        """Creates a new sudoku board by putting a digit into one of the free
        positions"""
        test_board = self.board.copy()
        test_board[position] = number
        return test_board

    def add_boards_to_guess_stack(self, board_position: BoardPosition):
        for test_num in board_position.possible_values:
            test_board = self.generate_test_board(board_position.position, test_num)
            self.guess_stack.append(test_board)

    def try_next_board_option(self) -> bool:
        try:
            self.board = self.guess_stack.pop()
        except IndexError:
            return False
        else:
            return True

    def position_with_fewest_options(
        self, options_for_all_positions: list[BoardPosition]
    ) -> BoardPosition | None:
        return min(
            options_for_all_positions, key=lambda x: x.options_count, default=None
        )

    def solve_sudoku(self, max_solutions) -> list[SudokuBoard]:
        """Try to solve any Sudoku board using 3 algorithms, alg1, alg2, and alg3"""

        while len(self.valid_solutions) < max_solutions:
            if "0" not in self.board and self.validate_complete_board():
                self.valid_solutions.append(self.board)
                if not self.try_next_board_option():
                    break

            self.reset_alg2()
            # Alg1
            empty_positions = self.get_options_for_free_positions()
            try:
                options_for_all_positions = self.fill_free_positions(empty_positions)
            except OutOfOptionsError:
                if not self.try_next_board_option():
                    break
                continue
            if options_for_all_positions is True:
                continue
            lowest = self.position_with_fewest_options(options_for_all_positions)

            # Alg 2
            if self.alg2():
                continue

            # Alg 3
            if lowest:
                self.add_boards_to_guess_stack(lowest)
            if not self.try_next_board_option():
                break

        return self.valid_solutions
