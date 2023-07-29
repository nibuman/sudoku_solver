from dataclasses import dataclass
from itertools import chain

SudokuBoard = list[str]
DigitsInPosition = set[str]
DigitsInPositions = list[DigitsInPosition]


class OutOfOptionsError(Exception):
    """No valid options for any digits in one or more positions of board"""


@dataclass
class BoardPosition:
    possible_values: DigitsInPosition
    position: int = 0

    @property
    def options_count(self):
        return len(self.possible_values)


class SudokuSolver:
    __version__ = "7.2"
    ALL_DIGITS = {str(n) for n in range(1, 10)}

    def __init__(self, board: str, max_solutions: int = 1) -> None:
        self.board = list(board)
        self.guess_stack: list[SudokuBoard] = []
        self.initialise_available_pos()
        self.difficulty_score = 0
        self.valid_solutions: list[SudokuBoard] = []
        self.max_solutions = max_solutions

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
        return None

    def update_alg2(self, position, available):
        alg2_rcs = self.get_rcs_alg2(position)
        for rcs in alg2_rcs:
            for num in available:
                rcs[int(num)].add(position)

    def get_sqr_index(self, row: int, col: int):
        """Identifies which 3x3 square (numbered 0-8) a given position is in:
        0 1 2
        3 4 5
        6 7 8
        e.g. position 0,3 will be square 0, 0,4 in square 1, and 8,7 in square 8.
        """
        return ((row // 3) * 3) + (col // 3)

    def get_index(self, position):
        """Returns 2d coordinates of position in r,c format"""
        r = position // 9
        c = position % 9
        return (r, c)

    def get_row(self, position: int) -> set:
        """Return set of numbers in row at given position"""
        r, _ = self.get_index(position)
        row_start = r * 9
        return set(self.board[row_start : row_start + 9])

    def get_col(self, position: int) -> set:
        """Return set of numbers in column at given position"""
        _, c = self.get_index(position)
        return {self.board[pos] for pos in range(c, 81, 9)}

    def get_sqr(self, position: int) -> set:
        """Return set of numbers in square at given position"""
        r, c = self.get_index(position)
        sq_start_pos = (r // 3) * 27 + (c // 3) * 3
        # offsets from starting position to visit every position in square
        offsets = (0, 1, 2, 9, 10, 11, 18, 19, 20)
        return {self.board[sq_start_pos + offset] for offset in offsets}

    def get_not_available(self, position: int) -> set[str]:
        """Return set of numbers that are not available in given position"""
        row = self.get_row(position)
        col = self.get_col(position)
        sqr = self.get_sqr(position)
        return set.union(row, col, sqr)

    def get_available(self, position: int) -> set[str]:
        """Return set of numbers that are available in a given position"""
        not_available = self.get_not_available(position)
        return self.ALL_DIGITS.difference(not_available)

    def check_valid(self) -> bool:
        """Checks whether sudoku board is valid by definition
        i.e. is there just one of each digit in each row, column and square"""
        if self.board is False:
            return False

        # check rows are valid
        for i in range(0, 81, 9):
            if self.get_row(i) != self.ALL_DIGITS:
                return False
        # check columns are valid
        for i in range(9):
            if self.get_col(i) != self.ALL_DIGITS:
                return False
        # check squares are valid
        for i in range(10, 81, 27):
            if self.get_sqr(i) != self.ALL_DIGITS:
                return False
        return True

    def get_options_for_free_positions(self):
        return [
            BoardPosition(
                possible_values=self.get_available(position), position=position
            )
            for position, num_str in enumerate(self.board)
            if num_str == "0"
        ]

    def fill_free_positions(self, free_positions: list[BoardPosition]):
        changed = False
        options = []
        for this_position in free_positions:
            match this_position.options_count:
                case 0:
                    raise OutOfOptionsError(
                        f"No options in position {this_position.position}"
                    )
                case 1:  # must be that number in this position
                    self.board[
                        this_position.position
                    ] = this_position.possible_values.pop()
                    changed = True
                case _:
                    options.append(this_position)
                    self.update_alg2(
                        this_position.position, this_position.possible_values
                    )
        position_with_fewest_options = min(
            options, key=lambda x: x.options_count, default=None
        )
        return changed or position_with_fewest_options

    def alg1(self):
        changed = False
        options = []
        for position, num_str in enumerate(self.board):
            if num_str != "0":
                continue
            current_postion = BoardPosition(
                possible_values=self.get_available(position), position=position
            )
            if current_postion.options_count == 0:  # must be an invalid board
                raise OutOfOptionsError(f"No options in position {position}")
            elif (
                current_postion.options_count == 1
            ):  # must be that number in this position
                self.board[position] = current_postion.possible_values.pop()
                changed = True
            else:
                options.append(current_postion)
                self.update_alg2(position, current_postion.possible_values)
        position_with_fewest_options = min(
            options, key=lambda x: x.options_count, default=None
        )
        return changed or position_with_fewest_options

    def alg2(self):
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

    def generate_test_board(self, position, number):
        test_board = self.board.copy()
        test_board[position] = number
        return test_board

    def alg3(self, lowest: BoardPosition, invalid_board=False):
        """Try each possible alternative value in turn using the board
        position with fewest alternatives to reduce the amount of recursion
        Last resort only runs if cannot fill numbers using other methods.
        """
        if not invalid_board and "0" in self.board:
            for test_num in lowest.possible_values:
                test_board = self.generate_test_board(lowest.position, test_num)
                self.guess_stack.append(test_board)
        try:
            self.board = self.guess_stack.pop()
        except IndexError:
            return False

        self.difficulty_score += 1
        self.initialise_available_pos()
        return True

    def solve_sudoku(self) -> list[SudokuBoard]:
        """Try to solve any Sudoku board using 3 algorithms, alg1, alg2, and alg3"""
        board_error = False

        while len(self.valid_solutions) < self.max_solutions:
            if "0" not in self.board:
                self.valid_solutions.append(self.board)
                try:
                    self.board = self.guess_stack.pop()
                except IndexError:
                    break

            self.reset_alg2()
            # Alg1
            board_error = False
            empty_positions = self.get_options_for_free_positions()
            try:
                result = self.fill_free_positions(empty_positions)
            except OutOfOptionsError:
                result = {"changed": False, "lowest": None}
                board_error = True
            if result is True:
                continue
            lowest = result

            # Alg 2
            if not board_error:
                if self.alg2():
                    continue

            # Alg 3
            result = self.alg3(lowest, invalid_board=board_error)
            if not result:
                break

        return self.valid_solutions
