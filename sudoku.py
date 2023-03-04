import json
import logging
import time
import argparse
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box

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
    if board_string[:6] == "preset":
        return get_test_sudokus(int(board_string[6]))
    allowed_vals = {str(n) for n in range(10)}
    board_list = [n for n in board_string if n in allowed_vals]
    if len(board_list) != 81:
        logging.error(f"Input board contains {len(board_list)} characters, 81 required")
        raise ValueError
    return board_list


def display_board_plain(board: str, solve_time: float, difficulty: int) -> None:
    """Display plain text Sudoku board in terminal"""
    output = ""
    for idx, num in enumerate(board):
        if idx % 27 == 0:  # A blank line after every 3 rows
            output += "\n\n"
        elif idx % 9 == 0:  # A newline at the end of every row
            output += "\n"
        elif idx % 3 == 0:  # A space between every 3 numbers
            output += " "
        output += num
    output += "\n"
    print(output)
    print(f"Solved in (ms): {1000*(solve_time):5.1f}\n" f"difficulty: {difficulty}")


def display_board_rich(
    input_board: str, solved_board: str, solve_time: float, difficulty: int
) -> None:
    """Display a formatted Sudoku board in the terminal using the rich library"""
    my_theme = Theme(
        {
            "input_number": "bold red on white",
            "standard": "bold black on white",
            "data": "blue on white",
            "title": "underline black on white",
        }
    )
    console = Console(theme=my_theme, width=28, style="standard")
    grid = Table(box=box.MINIMAL, show_header=False, expand=True)
    for _ in range(3):
        grid.add_column()
    text = ""
    sqr = []
    for idx, (input_num, solved_num) in enumerate(zip(input_board, solved_board)):
        if (
            idx % 3 == 0 and idx
        ):  # A space between every 3 numbers (but not before row 0)
            text += " "
            sqr.append(text)
            text = ""
        if idx % 9 == 0 and idx:  # Add completed row to grid
            grid.add_row(sqr[0], sqr[1], sqr[2])
            sqr.clear()
        if idx % 27 == 0 and idx:  # Add a line (new section) after every 3 rows
            grid.add_section()

        # Numbers that are in the input board display in a differnt style
        if int(input_num):
            this_theme = "[input_number]"
        else:
            this_theme = "[standard]"
        text += f"{this_theme} {solved_num}"

    # Just need to complete the last row
    text += " "
    sqr.append(text)
    grid.add_row(sqr[0], sqr[1], sqr[2])

    print_title = [
        "[title]Sudoku Solver",
    ]
    column = Columns(print_title, expand=True, align="center")
    console.print(column)
    console.print(grid)
    console.print(
        Panel(
            f"Speed: [data]{1000*(solve_time):5.1f} [standard]ms\n"
            f"Difficulty: [data]{difficulty}",
            title="Statistics",
        )
    )


def parse_commandline_args():
    parser = argparse.ArgumentParser(
        prog="sudoku", description="Solve any Sudoku puzzle"
    )
    input_parse_group = parser.add_mutually_exclusive_group(required=False)
    input_parse_group.add_argument(
        "-s",
        "--sudoku_string",
        action="store",
        help="use supplied Sudoku string",
        type=str,
    )
    input_parse_group.add_argument(
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
    output_parse_group = parser.add_mutually_exclusive_group(required=False)
    output_parse_group.add_argument(
        "-m",
        "--minimal",
        help="display only unformatted output string",
        action="store_true",
    )
    output_parse_group.add_argument(
        "-r",
        "--rich",
        help="display solution in rich text",
        action="store_true",
    )
    return parser.parse_args()


def main():
    args = parse_commandline_args()

    logging.basicConfig(
        filename="sudoku_solver.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )

    logging.info("Started")

    if args.preset is not None:
        sudoku_input = get_test_sudokus(args.preset)
    elif args.sudoku_string:
        sudoku_input = args.sudoku_string
    else:
        sudoku_input = input("Sudoku string: ")
        args.rich = True
    try:
        sudoku_input = valid_string(sudoku_input)
    except ValueError:
        logging.critical("Board string was not valid, exiting")
        exit("Invalid board")

    logging.info(f"Board to solve:{sudoku_input}")
    solver = SudokuSolver(sudoku_input)

    t1 = time.perf_counter()
    if solved_board := solver.solve_sudoku():
        t2 = time.perf_counter()
        solve_time = t2 - t1
        difficulty = solver.difficulty_score
        logging.info(f"Board solved in {solve_time} s")
        logging.info(f"Solution: {solved_board}")

        if args.minimal:
            print(solved_board)
        elif args.rich:
            display_board_rich(sudoku_input, solved_board, solve_time, difficulty)
        else:
            display_board_plain(solved_board, solve_time, difficulty)

    else:
        logging.warning("board: 0")


if __name__ == "__main__":
    main()
