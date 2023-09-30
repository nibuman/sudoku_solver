"""Loads Sudoku puzzles from the data file.

Data file contains various Sudoku puzzle inputs and answers
including puzzles with a single solution, multiple solutions,
and invalid boards. 'puzzles' are returned as a list of NamedTuple,
each with a single input board (question) and a list of solutions (answers),
even if there's only 1 solution.

Typical usage example:
    puzzle_num = 0
    input_board = data.valid_sudoku_puzzles()[puzzle_num].question
    expected_solution = data.valid_sudoku_puzzles()[puzzle_num].answers[0]
"""

import json
from typing import NamedTuple
from sudokusolve import config


class TestSudoku(NamedTuple):
    question: str
    answers: list[str]


def valid_sudoku_question(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the data file"""
    return valid_sudoku_puzzles()[puzzle_num].question


def valid_sudoku_puzzles() -> list[TestSudoku]:
    """Retrieves the test Sudoku boards from the data file"""
    return _get_sudoku_puzzles("single_solution_puzzles")


def invalid_sudoku_puzzles() -> list[TestSudoku]:
    """Retrieves a list of invalid completed boards from the data file"""
    return _get_sudoku_puzzles("invalid_boards")


def multiple_solution_puzzles() -> list[TestSudoku]:
    """Retrieves the test Sudoku boards from the data file"""
    return _get_sudoku_puzzles("multiple_solution_puzzles")


def _get_sudoku_puzzles(category: str) -> list[TestSudoku]:
    puzzles = _load_data()[category]
    return [
        TestSudoku(question=puzzle["question"], answers=puzzle["answers"])
        for puzzle in puzzles
    ]


def _load_data():
    with open(config.filepaths.data_file, "r") as f:
        data = json.load(f)
    return data
