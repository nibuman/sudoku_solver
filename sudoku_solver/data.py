import json
from sudoku_solver import config


def get_test_sudokus(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the config file"""
    with open(config.get_filepath("data"), "r") as f:
        config_data = json.load(f)
    return config_data["sudoku_puzzle"][puzzle_num]["question"]
