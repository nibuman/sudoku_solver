import pytest

from sudokusolve import data, validator
from sudokusolve.solver import solver_python_sets

DIGITS_1_9 = {str(n) for n in range(1, 10)}
SINGLE_SOLUTION_PUZZLES = data.valid_sudoku_puzzles()
STANDARD_VALID_INPUT = SINGLE_SOLUTION_PUZZLES[0].question
STANDARD_VALID_SOLVED = SINGLE_SOLUTION_PUZZLES[0].answers[0]


@pytest.fixture
def solver():
    return solver_python_sets.SudokuSolver()


@pytest.mark.parametrize(
    "position, expected_answer",
    [
        (0, (0, 0)),
        (1, (0, 1)),
        (9, (1, 0)),
        (20, (2, 2)),
    ],
)
def test_get_index(position, expected_answer):
    answer = solver_python_sets.SudokuSolver.get_index(position)
    assert answer == expected_answer


@pytest.mark.parametrize(
    "position, expected_answer",
    [
        (1, {"0", "3", "2", "6"}),
        (9, {"9", "0", "3", "5", "1"}),
        (80, {"5", "0", "1", "3"}),
    ],
)
def test_get_row(position, expected_answer, solver):
    solver.board = STANDARD_VALID_INPUT
    answer = solver.get_row(position)
    assert answer == expected_answer

    solver.board = STANDARD_VALID_SOLVED
    answer = solver.get_row(position)
    assert answer == DIGITS_1_9


@pytest.mark.parametrize(
    "position, expected_answer",
    [
        (1, {"0"}),
    ],
)
def test_get_col(position, expected_answer, solver):
    solver.board = STANDARD_VALID_INPUT
    answer = solver.get_col(position)
    assert answer == expected_answer

    solver.board = STANDARD_VALID_SOLVED
    answer = solver.get_col(position)
    assert answer == DIGITS_1_9


@pytest.mark.parametrize(
    "position, expected_answer",
    [
        (1, {"3", "0", "9", "1"}),
        (3, {"0", "2", "3", "5", "8", "6"}),
        (13, {"0", "2", "3", "5", "8", "6"}),
        (23, {"0", "2", "3", "5", "8", "6"}),
        (28, {"0", "8", "7", "6"}),
        (80, {"5", "0", "9", "3"}),
    ],
)
def test_get_sqr(position, expected_answer, solver):
    solver.board = STANDARD_VALID_INPUT
    answer = solver.get_sqr(position)
    assert answer == expected_answer

    solver.board = STANDARD_VALID_SOLVED
    answer = solver.get_sqr(position)
    assert answer == DIGITS_1_9

