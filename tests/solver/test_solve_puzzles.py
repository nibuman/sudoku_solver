import pytest
from sudokusolve import data, validator

from sudokusolve.solver import solver_python_gen, solver_python_sets

SINGLE_SOLUTION_PUZZLES = data.valid_sudoku_puzzles()
STANDARD_VALID_INPUT = SINGLE_SOLUTION_PUZZLES[0].question
STANDARD_VALID_SOLVED = SINGLE_SOLUTION_PUZZLES[0].answers[0]


@pytest.fixture(params=[solver_python_gen, solver_python_sets.SudokuSolver()])
def solver(request):
    return request.param.solve_sudoku

@pytest.fixture
def completed_board_validator():
    return validator.validate_solved_board


@pytest.mark.parametrize("puzzle_number", [0, 1, 2, 3, 4, 5, 6])
def test_solve_sudoku(puzzle_number, solver, completed_board_validator):
    input_board = SINGLE_SOLUTION_PUZZLES[puzzle_number].question
    expected_answer = SINGLE_SOLUTION_PUZZLES[puzzle_number].answers[0]
    # Test with the built in validator and max_solution set to 1
    answer = solver(input_board, completed_board_validator, 1)[0]
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
    answer = solver(input_board, lambda _: True, 1)[0]
    assert answer == expected_answer


@pytest.mark.parametrize("puzzle_number", [0, 1, 2, 3, 4, 5, 6])
def test_solve_sudoku_single_answer(puzzle_number, solver, completed_board_validator):
    # Now test the same puzzle but with a validator that returns True
    # without checking...
    input_board = SINGLE_SOLUTION_PUZZLES[puzzle_number].question
    expected_answer = SINGLE_SOLUTION_PUZZLES[puzzle_number].answers[0]
    # Test with the built in validator and max_solution set to 2
    answers = solver(input_board, completed_board_validator, 2)
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
    answers = solver(
        input_board, completed_board_validator, len(expected_answers) + 1
    )
    assert len(answers) == len(expected_answers)
    assert all(expected_answer in answers for expected_answer in expected_answers)
    assert all(answer in expected_answers for answer in answers)
