import pytest
from sudoku_solver import validator, data

DIGITS_1_9 = {str(n) for n in range(1, 10)}
DIGITS_0_9 = {str(n) for n in range(10)}
SINGLE_SOLUTION_PUZZLES = data.valid_sudoku_puzzles()
STANDARD_VALID_INPUT = SINGLE_SOLUTION_PUZZLES[0].question
STANDARD_VALID_SOLVED = SINGLE_SOLUTION_PUZZLES[0].answers[0]
INVALID_BOARD_SOLVED = data.invalid_sudoku_puzzles()[0].answers[0]


@pytest.mark.parametrize(
    "board, expected_answer",
    [("0" * 81, True), ("", False), ("0" * 80, False)],
    ids=["zeros", "empty", "too short"],
)
def test_correct_number_of_digits(board, expected_answer):
    assert validator._correct_number_of_digits(board) == expected_answer


def test_get_all_squares():
    board = "1" * 81
    assert len(validator._get_all_squares(board)) == 9


def test_only_valid_digits():
    board = "".join([str(row_num) for row_num in range(9) for _ in range(9)])
    assert validator._only_valid_digits(board, DIGITS_0_9)

    invalid_board = f"{board[0:80]}a"
    assert not validator._only_valid_digits(invalid_board, DIGITS_0_9)


@pytest.mark.parametrize(
    "board, expected_answer",
    [
        ("", False),
        ("0" * 82, False),
        ("1" + ("0" * 80), True),
        ("0" * 81, True),
        (STANDARD_VALID_INPUT, True),
        (INVALID_BOARD_SOLVED, False),
    ],
    ids=[
        "empty",
        "too long",
        "1 + zeros",
        "zeros",
        "valid input board",
        "invalid solved board",
    ],
)
def test_validate_input_board(board, expected_answer):
    assert validator.validate_input_board(board) == expected_answer


@pytest.mark.parametrize(
    "board, expected_answer",
    [
        ("1" * 81, False),
        (STANDARD_VALID_SOLVED, True),
        (INVALID_BOARD_SOLVED, False),
    ],
    ids=["ones", "board 0", "invalid board"],
)
def test_validate_solved_board(board, expected_answer):
    assert validator.validate_solved_board(board) == expected_answer
