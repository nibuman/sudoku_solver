from typing import Callable
import logging


class SudokuValidator:
    DIGITS_1_TO_9 = {str(n) for n in range(1, 10)}
    DIGITS_0_TO_9 = {str(n) for n in range(10)}

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
                self.digits_present_only_once(board, self.get_all_rows),  # Rows
                self.digits_present_only_once(board, self.get_all_columns),  # Columns
                self.digits_present_only_once(board, self.get_all_squares),  # Squares
            ]
        )

    def validate_solved_board(self, board: str) -> bool:
        """Checks whether sudoku board is valid by definition
        i.e. is there exactly one of each digit in each row, column and square"""
        return all(
            [
                self.correct_number_of_digits(board),
                self.all_digits_present(board, self.get_all_rows),  # Rows
                self.all_digits_present(board, self.get_all_columns),  # Columns
                self.all_digits_present(board, self.get_all_squares),  # Squares
            ]
        )

    def clean_string(self, board_string: str) -> str:
        """Reformats a text string as a valid board definition
        - will remove any characters that are not 0-9
        Checks that final string is the correct length (81)
        """
        ALLOWED_VALUES = {str(n) for n in range(10)}
        cleaned_board = "".join([n for n in board_string if n in ALLOWED_VALUES])
        if len(cleaned_board) != 81:
            logging.error(
                f"Input board contains {len(cleaned_board)} characters, 81 required"
            )
            raise ValueError
        return cleaned_board

    @staticmethod
    def get_all_rows(board):
        return [board[i : i + 9] for i in range(0, 81, 9)]

    @staticmethod
    def get_all_columns(board):
        return [board[i::9] for i in range(9)]

    @staticmethod
    def get_all_squares(board):
        offsets = (0, 1, 2, 9, 10, 11, 18, 19, 20)
        squares = []
        for a in range(0, 81, 27):
            for b in range(0, 9, 3):
                squares.append("".join([board[a + b + o] for o in offsets]))
        return squares

    @staticmethod
    def only_valid_digits(board: str, valid_digits: set[str]) -> bool:
        return all(d in valid_digits for d in board)

    @staticmethod
    def correct_number_of_digits(board: str) -> bool:
        return len(board) == 81

    def all_digits_present(
        self, board: str, get_rcs: Callable[[str], list[str]]
    ) -> bool:
        """Check that all the digits and only the valid digit are present in
        each area (row, column or square). Accepts a function that returns the set
        of numbers in a given row/column/square and a sequence of the indices
        of each row/column/square to check"""
        return all(set(list(rcs)) == self.DIGITS_1_TO_9 for rcs in get_rcs(board))

    def digits_present_only_once(self, board: str, get_rcs: Callable) -> bool:
        """Check that digits are present at most once in each area (row,
        column, or square)"""
        digits_present_only_once = []
        for rcs in get_rcs(board):
            digits_without_zero = [d for d in rcs if d != "0"]
            digits_present_only_once.append(
                sorted(digits_without_zero) == sorted(list(set(digits_without_zero)))
            )
        print(digits_present_only_once)
        return all(digits_present_only_once)
