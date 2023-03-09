import json
import logging
import time
import argparse
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.live import Live
from rich import box
from rich.layout import Layout
from sudoku_solver import SudokuSolver


class SudokuBoardDisplay:
    def __init__(
        self, input_board: str, solved_board: str, solve_time: float, difficulty: int
    ) -> None:
        self.input_board = input_board
        self.solved_board = solved_board
        self.all_positions = set(range(81))
        self.display_positions = set()
        self.solve_time = solve_time
        self.difficulty = difficulty
        self.theme = Theme(
            {
                "input_number": "bold red on white",
                "standard": "bold black on white",
                "data": "blue on white",
                "title": "underline black on white",
            }
        )

    def display_minimal(self) -> None:
        print(self.solved_board)

    def display_plain(self) -> None:
        """Display plain text Sudoku board in terminal"""
        output = ""
        for idx, num in enumerate(self.solved_board):
            if idx % 27 == 0:  # A blank line after every 3 rows
                output += "\n\n"
            elif idx % 9 == 0:  # A newline at the end of every row
                output += "\n"
            elif idx % 3 == 0:  # A space between every 3 numbers
                output += " "
            output += num
        output += "\n"
        print(output)
        print(
            f"Solved in (ms): {1000*(self.solve_time):5.1f}\n"
            f"difficulty: {self.difficulty}"
        )

    def display_rich_static(self) -> None:
        """Display a formatted Sudoku board in the terminal using the rich library"""
        console = Console(theme=self.theme, height=18, width=30, style="standard")
        layout = Layout()

        # Title
        title = Align("[title]Sudoku Solver[/title]", align="center")

        # Sudoku grid
        grid = self.rich_sudoku_grid()

        # Statistics panel
        statistics = Panel(
            f"Speed: [data]{1000*(self.solve_time):5.1f} [standard]ms\n"
            f"Difficulty: [data]{self.difficulty}[/data]",
            title="Statistics",
        )

        layout.split_column(
            Layout(title, name="title", size=1),
            Layout(grid, name="grid", size=13),
            Layout(statistics, name="stats", size=4),
        )
        console.print(layout)

    def display_rich_animated(self) -> None:
        """Display a formatted Sudoku board in the terminal using the rich library"""
        console = Console(theme=self.theme, height=18, width=28, style="standard")
        layout = Layout()

        # Title
        title = Align("[title]Sudoku Solver[/title]", align="center", style="standard")

        # Sudoku grid
        grid = self.rich_sudoku_grid()
        grid.style = "standard"
        # Statistics panel
        statistics = Panel(
            f"Speed: [data]{1000*(self.solve_time):5.1f} [standard]ms\n"
            f"Difficulty: [data]{self.difficulty}[/data]",
            title="Statistics",
            style="standard",
        )

        layout.split_column(
            Layout(title, name="title", size=1),
            Layout(grid, name="grid", size=13),
            Layout(statistics, name="stats", size=4),
        )

        with Live(
            layout,
            console=console,
            screen=False,
            refresh_per_second=4,
        ) as live:  # update 4 times a second to feel fluid
            # live.console.print(layout)
            time.sleep(1)
            title = Align(
                "[title]Sudoku Solved[/title]", align="center", style="standard"
            )
            layout["title"].update(title)
            time.sleep(2)

    def rich_sudoku_grid(self):
        grid = Table(
            box=box.MINIMAL,
            show_header=False,
            expand=False,
            style="standard",
            collapse_padding=True,
        )
        for _ in range(3):
            grid.add_column()
        sqr = []
        cols = []
        for idx, (input_num, solved_num) in enumerate(
            zip(self.input_board, self.solved_board)
        ):
            if (
                idx % 3 == 0 and idx
            ):  # A space between every 3 numbers (but not before row 0)
                sqr.append(Columns(cols, padding=(0, 1)))
                cols.clear()
            if idx % 9 == 0 and idx:  # Add completed row to grid
                self.add_rows_to_grid(grid, sqr)
                sqr.clear()
            if idx % 27 == 0 and idx:  # Add a line (new section) after every 3 rows
                grid.add_section()
            cols.append(self.grid_numbers(input_num, solved_num))
        # Just need to complete the last row
        sqr.append(Columns(cols, padding=(0, 1)))
        self.add_rows_to_grid(grid, sqr)
        return grid

    def add_rows_to_grid(self, grid: Table, sqr):
        grid.add_row(
            Align(sqr[0], align="center"),
            Align(sqr[1], align="center"),
            Align(sqr[2], align="center"),
            style="standard",
        )

    def grid_numbers(self, input_num, solved_num):
        # Numbers that are in the input board display in a differnt style
        if int(input_num):
            style = "input_number"

        else:
            style = "standard"
        return f"[{style}]{solved_num}[/{style}]"


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


def parse_commandline_args():
    parser = argparse.ArgumentParser(
        prog="sudoku", description="Solve any Sudoku puzzle"
    )
    input_parse_group = parser.add_mutually_exclusive_group(required=False)
    input_parse_group.add_argument(
        "-s",
        "--sudoku-string",
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
        "-u",
        "--unformatted",
        help="display solution in unformatted plain text",
        action="store_true",
    )
    output_parse_group.add_argument(
        "-r",
        "--rich",
        help="display solution in rich text",
        action="store_true",
    )
    output_parse_group.add_argument(
        "-a",
        "--animated",
        help="display solution with animation",
        action="store_true",
    )
    return parser.parse_args()


def get_user_input() -> str:
    if Confirm.ask("Use a preset Sudoku board?", default="y", show_default=True):
        preset = IntPrompt.ask(
            "Enter preset number",
            choices=["0", "1", "2", "3", "4", "5", "6"],
            default=0,
            show_default=True,
        )
        return get_test_sudokus(preset)
    else:
        return Prompt.ask("Enter Sudoku board")


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
        sudoku_input = get_user_input()
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

        board = SudokuBoardDisplay(sudoku_input, solved_board, solve_time, difficulty)
        if args.minimal:
            board.display_minimal()
        elif args.unformatted:
            board.display_plain()
        elif args.rich:
            board.display_rich_static()
        else:
            board.display_rich_animated()

    else:
        logging.warning("board: 0")


if __name__ == "__main__":
    main()
