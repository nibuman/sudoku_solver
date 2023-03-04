import json
import logging
import time
import argparse

from sudoku_solver import SudokuSolver


def get_test_sudokus(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the config file"""
    assert 0 <= puzzle_num < 7, f"Test Sudoku must be 0-6,{puzzle_num} given"
    with open("./sudoku_data.json", "r") as f:
        config_data = json.load(f)
    return config_data["sudoku_puzzle"][puzzle_num]["question"]


def valid_string(board_string: str) -> list:
    """Reformats a text string as a valid board definition
    - will remove any characters that are not 0-9
    Checks that final list is the correct length (81)
    """

    allowed_vals = {str(n) for n in range(10)}
    board_list = [n for n in board_string if n in allowed_vals]
    if len(board_list) != 81:
        logging.error(f"Input board contains {len(board_list)} characters, 81 required")
        raise ValueError
    return board_list


def main():
    parser = argparse.ArgumentParser(
        prog="sudoku", description="Solve any Sudoku puzzle"
    )
    parse_group = parser.add_mutually_exclusive_group(required=False)
    parse_group.add_argument(
        "-s",
        "--sudoku_string",
        action="store",
        help="use supplied Sudoku string",
        type=str,
    )
    parse_group.add_argument(
        "-p",
        "--preset",
        help="use preset Sudoku board 1-6",
        action="store",
        choices=range(0, 7),
        type=int,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + SudokuSolver.__version__,
    )
    parser.add_argument(
        "-q", "--quiet", help="display only output string", action="store_true"
    )
    args = parser.parse_args()

    logging.basicConfig(
        filename="sudoku_solver.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )

    logging.info("Started")

    if args.quiet:
        quiet = True
    if args.preset is not None:
        sudoku_input = get_test_sudokus(args.preset)
    elif args.sudoku_string:
        sudoku_input = args.sudoku_string
    else:
        sudoku_input = input("Sudoku string: ")
    try:
        board_list = valid_string(sudoku_input)
    except ValueError:
        logging.critical("Board string was not valid, exiting")
        exit("Invalid board")

    logging.info(f'Board to solve:{"".join(board_list)}')
    board = SudokuSolver(list(sudoku_input))

    t1 = time.perf_counter()
    if solved_board := board.solve_sudoku():
        t2 = time.perf_counter()
        logging.info(f"Board solved in {t2-t1} s")
        logging.info(f"Solution: {solved_board}")

        if quiet:
            print(solved_board)
        else:
            print(
                f"board: {solved_board}\n"
                f"Solved in (ms): {1000*(t2 - t1):5.1f}\n"
                f"difficulty: {board.difficulty_score}"
            )
    else:
        logging.warning("board: 0")


if __name__ == "__main__":
    main()
