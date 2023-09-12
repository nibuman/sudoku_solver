import json
from typing import NamedTuple
from sudoku_solver import config


class TestSudoku(NamedTuple):
    question: str
    answers: list[str]


def valid_sudoku_question(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the config file"""
    return valid_sudoku_puzzles()[puzzle_num].question


def valid_sudoku_puzzles() -> list[TestSudoku]:
    """Retrieves the test Sudoku boards from the config file"""
    return _get_sudoku_puzzles("single_solution_puzzles")


def multiple_solution_puzzles() -> list[TestSudoku]:
    """Retrieves the test Sudoku boards from the config file"""
    return _get_sudoku_puzzles("multiple_solution_puzzles")


def _get_sudoku_puzzles(category: str) -> list[TestSudoku]:
    puzzles = _load_data()[category]
    return [
        TestSudoku(question=puzzle["question"], answers=puzzle["answers"])
        for puzzle in puzzles
    ]


def _load_data():
    with open(config.get_filepath("data"), "r") as f:
        config_data = json.load(f)
    return config_data
