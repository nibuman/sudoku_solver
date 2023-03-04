import logging
import numpy as np


class SudokuSolver:
    __version__ = "6.3"

    def __init__(self, board) -> None:
        self.board = self.array_from_list(board)
        self.guess_stack = []
        self.initialise_available_pos()
        self.difficulty_score = 0

    def initialise_available_pos(self):
        self.available_pos_row = [[set() for _ in range(10)] for _ in range(9)]
        self.available_pos_col = [[set() for _ in range(10)] for _ in range(9)]
        self.available_pos_sqr = [[set() for _ in range(10)] for _ in range(9)]

    def get_rcs_alg2(self, position: int) -> tuple:
        """Returns the row, column and square for a particular cell for alg2"""
        r, c = self.get_index(position)
        s = self.get_sqr_index(position)
        return (
            self.available_pos_row[r],
            self.available_pos_col[c],
            self.available_pos_sqr[s],
        )

    def reset_alg2(self):
        """Clears all the available positions used in alg2"""
        for alg2_rcs in (
            self.available_pos_row,
            self.available_pos_col,
            self.available_pos_sqr,
        ):
            for rcs in alg2_rcs:
                for position_set in rcs:
                    position_set.clear()

    def update_alg2(self, position, available):
        alg2_rcs = self.get_rcs_alg2(position)
        for rcs in alg2_rcs:
            for num in available:
                rcs[int(num)].add(position)

    def get_sqr_index(self, position):
        """Identifies which 3x3 square (numbered 0-8) a given position is in:
        0 1 2
        3 4 5
        6 7 8
        e.g. position 3 will be square 0, 4 in square 1, and 80 in square 8.
        """
        r, c = self.get_index(position)
        return ((r // 3) * 3) + (c // 3)

    def get_index(self, position):
        """Returns 2d coordinates of position in r,c format"""
        r = position // 9
        c = position % 9
        return (r, c)

    def get_row(self, position: int) -> set:
        """Return set of numbers in row at given position"""
        r, _ = self.get_index(position)
        return set(self.board[r, :])

    def get_col(self, position: int) -> set:
        """Return set of numbers in column at given position"""
        _, c = self.get_index(position)
        return set(self.board[:, c])

    def get_sqr(self, position: int) -> set:
        """Return set of numbers in square at given position"""
        r, c = self.get_index(position)
        sq_row = (r // 3) * 3
        sq_col = (c // 3) * 3
        return set(self.board[sq_row : sq_row + 3, sq_col : sq_col + 3].flatten())

    def get_not_available(self, position: int) -> set:
        """Return set of numbers that are not available in given position"""
        row = self.get_row(position)
        col = self.get_col(position)
        sqr = self.get_sqr(position)
        return set.union(row, col, sqr)

    def get_available(self, position: int) -> set:
        """Return set of numbers that are available in a given position"""
        all_digits = {str(n) for n in range(1, 10)}
        not_available = self.get_not_available(position)
        return all_digits.difference(not_available)

    def update_board(self, position: int, number: str) -> None:
        """Places a number in the board"""
        r, c = self.get_index(position)
        self.board[r, c] = number

    def get_position(self, position: int) -> str:
        """Returns number at given position in board"""
        r, c = self.get_index(position)
        return self.board[r, c]

    def check_valid(self) -> bool:
        """Checks whether sudoku board is valid by definition
        i.e. is there just one of each digit in each row, column and square"""
        if self.board is False:
            return False
        valid_set = {str(n) for n in range(1, 10)}

        # check rows are valid
        for i in range(0, 81, 9):
            if self.get_row(i) != valid_set:
                return False
        # check columns are valid
        for i in range(9):
            if self.get_col(i) != valid_set:
                return False
        # check squares are valid
        for i in range(0, 81, 12):
            if self.get_sqr(i) != valid_set:
                return False
        return self.get_string()

    def get_string(self) -> str:
        """Returns board as string"""
        return "".join(self.board.flatten())

    def array_from_list(self, board_list):
        """Returns 1d list as 2d NumPy array"""
        return np.reshape(board_list, (9, 9))

    def alg1(self):
        changed = False
        board_error = False
        lowest = {"position": 0, "count": 9, "values": {}}
        for position, num_str in enumerate(self.board.flatten()):
            if num_str != "0":
                continue
            available = self.get_available(position)
            available_count = len(available)

            if available_count == 0:  # must be an invalid board
                logging.warning(f"[alg1] available_count == 0 in pos {position}")
                board_error = True
                break
            if available_count == 1:  # must be that number in this position
                self.update_board(position, available.pop())
                changed = True
                logging.debug(
                    f"[alg1] Assigned {self.get_position(position)}"
                    f" to position {position}"
                )
                # self.update_available(position, board[position])
            else:
                if available_count < lowest["count"]:
                    lowest["count"] = available_count
                    lowest["position"] = position
                    lowest["values"] = available.copy()
                self.update_alg2(position, available)

        return {"changed": changed, "error": board_error, "lowest": lowest}

    def alg2(self):
        """run the second algorithm - each row, col, sq must have 1 of all 9 numbers"""
        changed = False
        for alg2_rcs in (
            self.available_pos_row,
            self.available_pos_col,
            self.available_pos_sqr,
        ):
            for rcs in alg2_rcs:
                for number, available_pos in enumerate(rcs):
                    if len(available_pos) == 1 and number != "0":
                        position = available_pos.pop()
                        self.update_board(position, str(number))
                        logging.debug(
                            f"[alg2] Assigned"
                            f"{self.get_position(position)} to position"
                            f"{position}"
                        )
                        changed = True
        return changed

    def generate_test_board(self, position, number):
        test_board = self.board.copy()
        r, c = self.get_index(position)
        test_board[r, c] = number
        return test_board

    def alg3(self, lowest=None, invalid_board=False):
        """Try each possible alternative value in turn using the board
        position with fewest alternatives to reduce the amount of recursion
        Last resort only runs if cannot fill numbers using other methods.
        """
        if not invalid_board:
            for test_num in lowest["values"]:
                test_board = self.generate_test_board(lowest["position"], test_num)
                self.guess_stack.append(test_board)
        try:
            self.board = self.guess_stack.pop()
            self.difficulty_score += 1

        except IndexError:
            return False
        self.initialise_available_pos()
        return True

    def solve_sudoku(self) -> list:
        """Try to solve any Sudoku board, needs to be called for each guess
        - Iterates through every cell
        - Removes any values already used in each row, column or square
        - If only one value possible for a cell - then assign that
        - If no previous iterations don't find any valid values then:
        - Try different values
        """

        board_error = False
        # sudoku = SudokuBoard(board)

        logging.debug("[solve_sudoku] Entering solve_sudoku.")

        while "0" in self.board:
            self.reset_alg2()
            # Alg1
            result = self.alg1()
            board_error = result["error"]
            if result["changed"] is True:
                continue
            lowest = result["lowest"]

            # Alg 2
            if not board_error:
                if self.alg2():
                    continue

            # Alg 3
            result = self.alg3(lowest, invalid_board=board_error)
            if not result:
                return False

        return self.check_valid()
