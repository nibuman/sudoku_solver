"""Checks that sudoku board strings are valid.

Functions to check that both input and solved Sudoku boards supplied
as strings are valid, e.g. correct length, only valid digits present,
and that there is exactly one of each digit in each row, column and square
for solved boards and no more than one for an input board (except for "0")

Typical usage example:

    if validate_input_board(my_input_board):
        do stuff

    if validate_solved_board(my_solved_board):
        do other stuff
"""
from typing import Callable


DIGITS_1_TO_9 = {str(n) for n in range(1, 10)}
DIGITS_0_TO_9 = {str(n) for n in range(10)}


def validate_input_board(board: str) -> bool:
    """Check that input board is valid."""

    # Need to check that the string is the correct length and valid first,
    # or get an index error when the `_get_all_*` functions in the arguments are
    # evaluated. Also why need to carry out lazy evaluation in a generator...
    return all(
        func(*args)
        for func, args in [
            (_correct_number_of_digits, (board,)),
            (_only_digits_0_9, (board,)),
            (_digits_present_only_once, (board, _get_all_rows)),
            (_digits_present_only_once, (board, _get_all_columns)),
            (_digits_present_only_once, (board, _get_all_squares)),
        ]
    )


def validate_solved_board(board: str) -> bool:
    """Checks whether solved sudoku board is valid.

    Board must have 81 digits, exactly one of each digit in each row, column and square.
    Needs lazy evaluation in generator as early evalution of _get_all_* functions will lead
    to index error if _correct_number_of_digits not evaluated first.
    """
    return all(
        func(*args)
        for func, args in [
            (_correct_number_of_digits, (board,)),
            (_all_digits_present, (board, _get_all_rows)),
            (_all_digits_present, (board, _get_all_columns)),
            (_all_digits_present, (board, _get_all_squares)),
        ]
    )


def clean_string(board_string: str) -> str:
    """Reformats a text string as a valid board definition
    - removes any characters that are not digits 0-9
    """
    return "".join([n for n in board_string if n in DIGITS_0_TO_9])


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


def _only_digits_0_9(board) -> bool:
    return all(d in DIGITS_0_TO_9 for d in board)


def _correct_number_of_digits(board) -> bool:
    return len(board) == 81


def _all_digits_present(board: str, get_rcs: Callable[[str], list[str]]) -> bool:
    """get_rcs: accepts a function that returns a list of digits as strings"""
    return all(set(list(rcs)) == DIGITS_1_TO_9 for rcs in get_rcs(board))


def _digits_present_only_once(board: str, get_rcs: Callable[[str], list[str]]) -> bool:
    return all(rcs.count(d) < 2 for rcs in get_rcs(board) for d in DIGITS_1_TO_9)
