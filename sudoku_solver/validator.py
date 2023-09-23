from typing import Callable


DIGITS_1_TO_9 = {str(n) for n in range(1, 10)}
DIGITS_0_TO_9 = {str(n) for n in range(10)}


def validate_input_board(board: str) -> bool:
    # TODO: docstring
    # TODO: combine the 2 all expressions
    if not all(
        [
            _correct_number_of_digits(board),
            _only_valid_digits(board, DIGITS_0_TO_9),
        ]
    ):
        return False

    return all(
        [
            _digits_present_only_once(board, _get_all_rows),
            _digits_present_only_once(board, _get_all_columns),
            _digits_present_only_once(board, _get_all_squares),
        ]
    )


def validate_solved_board(board: str) -> bool:
    """Checks whether solved sudoku board is valid by definition:
    - 81 digits
    - exactly one of each digit in each row, column and square
    """
    return all(
        [
            _correct_number_of_digits(board),
            _all_digits_present(board, _get_all_rows),
            _all_digits_present(board, _get_all_columns),
            _all_digits_present(board, _get_all_squares),
        ]
    )


def clean_string(board_string: str) -> str:
    """Reformats a text string as a valid board definition
    - removes any characters that are not digits 0-9
    """
    ALLOWED_VALUES = {str(n) for n in range(10)}
    cleaned_board = "".join([n for n in board_string if n in ALLOWED_VALUES])
    return cleaned_board


def _get_all_rows(board):
    return [board[i : i + 9] for i in range(0, 81, 9)]


def _get_all_columns(board):
    return [board[i::9] for i in range(9)]


def _get_all_squares(board):
    offsets = (0, 1, 2, 9, 10, 11, 18, 19, 20)
    squares = []
    for a in range(0, 81, 27):
        for b in range(0, 9, 3):
            squares.append("".join([board[a + b + o] for o in offsets]))
    return squares


def _only_valid_digits(board, valid_digits) -> bool:
    return all(d in valid_digits for d in board)


def _correct_number_of_digits(board) -> bool:
    return len(board) == 81


def _all_digits_present(board: str, get_rcs: Callable[[str], list[str]]) -> bool:
    """get_rcs: accepts a function that returns a list of digits as strings"""
    return all(set(list(rcs)) == DIGITS_1_TO_9 for rcs in get_rcs(board))


def _digits_present_only_once(board: str, get_rcs: Callable[[str], list[str]]) -> bool:
    digits_present_only_once = []
    for rcs in get_rcs(board):
        digits_without_zero = [d for d in rcs if d != "0"]
        digits_present_only_once.append(
            sorted(digits_without_zero) == sorted(list(set(digits_without_zero)))
        )
    return all(digits_present_only_once)
