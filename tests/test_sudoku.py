from sudokusolve import data, config
import pytest
import subprocess


def puzzle_solution(puzzle_num):
    return data.valid_sudoku_puzzles()[puzzle_num].answers[0]


@pytest.mark.parametrize(
    "puzzle_number, expected_answer",
    [(puzzle_num, puzzle_solution(puzzle_num)) for puzzle_num in range(7)],
)
def test_main(puzzle_number, expected_answer, capsys):
    captured = subprocess.run(
        [
            "python3",
            config.filepaths.parent_directory,
            "-b",
            str(puzzle_number),
            "-u",
            "unformatted_CLI",
        ],
        capture_output=True,
        text=True,
    )
    assert captured.stdout == f"{expected_answer}\n"
