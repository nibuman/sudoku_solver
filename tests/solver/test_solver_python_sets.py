import pytest
from sudoku_solver import data, validator
from sudoku_solver.solver import solver_python_sets

DIGITS_1_9 = {str(n) for n in range(1, 10)}
SINGLE_SOLUTION_PUZZLES = data.valid_sudoku_puzzles()
STANDARD_VALID_INPUT = SINGLE_SOLUTION_PUZZLES[0].question
STANDARD_VALID_SOLVED = SINGLE_SOLUTION_PUZZLES[0].answers[0]


@pytest.fixture
def solver():
    return solver_python_sets.SudokuSolver()


@pytest.fixture
def completed_board_validator():
    return validator.validate_solved_board


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


@pytest.mark.parametrize("puzzle_number", [0, 1, 2, 3, 4, 5, 6])
def test_solve_sudoku(puzzle_number, solver, completed_board_validator):
    input_board = SINGLE_SOLUTION_PUZZLES[puzzle_number].question
    expected_answer = SINGLE_SOLUTION_PUZZLES[puzzle_number].answers[0]
    # Test with the built in validator and max_solution set to 1
    answer = solver.solve_sudoku(input_board, completed_board_validator, 1)[0]
    assert answer == expected_answer


@pytest.mark.parametrize(
    "puzzle_number",
    [
        0,
        1,
        2,
        3,
        pytest.param(4, marks=pytest.mark.xfail),
        pytest.param(5, marks=pytest.mark.xfail),
        6,
    ],
)
def test_solve_sudoku_no_validator(puzzle_number, solver):
    # Now test the same puzzle but with a validator that returns True
    # without checking...
    input_board = SINGLE_SOLUTION_PUZZLES[puzzle_number].question
    expected_answer = SINGLE_SOLUTION_PUZZLES[puzzle_number].answers[0]
    answer = solver.solve_sudoku(input_board, lambda _: True, 1)[0]
    assert answer == expected_answer


@pytest.mark.parametrize("puzzle_number", [0, 1, 2, 3, 4, 5, 6])
def test_solve_sudoku_single_answer(puzzle_number, solver, completed_board_validator):
    # Now test the same puzzle but with a validator that returns True
    # without checking...
    input_board = SINGLE_SOLUTION_PUZZLES[puzzle_number].question
    expected_answer = SINGLE_SOLUTION_PUZZLES[puzzle_number].answers[0]
    # Test with the built in validator and max_solution set to 2
    answers = solver.solve_sudoku(input_board, completed_board_validator, 2)
    assert answers[0] == expected_answer
    assert len(answers) == 1


@pytest.mark.parametrize("puzzle_number", [0])
def test_solve_sudoku_multiple_answers(
    puzzle_number, solver, completed_board_validator
):
    # Now test the same puzzle but with a validator that returns True
    # without checking...
    puzzle = data.multiple_solution_puzzles()[puzzle_number]
    input_board = puzzle.question
    expected_answers = puzzle.answers
    # Test with the built in validator and max_solution set to 2
    answers = solver.solve_sudoku(
        input_board, completed_board_validator, len(expected_answers) + 1
    )
    assert len(answers) == len(expected_answers)
    assert all(expected_answer in answers for expected_answer in expected_answers)
    assert all(answer in expected_answers for answer in answers)
