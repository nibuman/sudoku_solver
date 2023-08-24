import json
import logging
import time
import argparse
import random
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
from sudoku_solver import plugins, validator
from sudoku_solver.ui import ui_simple_CLI as ui
from sudoku_solver.solver import solver_python_sets as solver


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
                "empty_pos": "grey50 on white",
            }
        )

    def display_minimal(self) -> None:
        print(self.solved_board)

    def display_rich_static(self) -> None:
        """Display a formatted Sudoku board in the terminal using the rich library"""
        console = Console(theme=self.theme, height=18, width=30, style="standard")
        layout = Layout()

        # Title
        title = Align("[title]Sudoku Solver[/title]", align="center")

        # Sudoku grid
        self.display_positions = self.all_positions
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
        self.display_positions = {
            idx for idx, num in enumerate(self.input_board) if int(num)
        }
        self.remaining_positions = self.all_positions.difference(self.display_positions)
        grid = self.rich_sudoku_grid(empty_pos=lambda: " ")
        grid.style = "standard"

        # Statistics panel
        statistics = Panel(
            "Speed:     ms\nDifficulty: ",
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
            refresh_per_second=24,
        ):  # update 4 times a second to feel fluid
            # live.console.print(layout)
            time.sleep(0.5)
            title = Align(
                "[title]Sudoku Solved[/title]", align="center", style="standard"
            )
            while self.remaining_positions:
                next_pos = random.choice(list(self.remaining_positions))
                self.remaining_positions.discard(next_pos)
                self.display_positions.add(next_pos)
                grid = self.rich_sudoku_grid(
                    empty_pos=lambda: random.choice(list(range(1, 10)))
                )
                layout["grid"].update(grid)
                time.sleep(0.05)

                # Statistics panel
            statistics = Panel(
                f"[standard]Speed: [data]{1000*(self.solve_time):5.1f} [standard]ms\n"
                f"[standard]Difficulty: [data]{self.difficulty}[/data]",
                title="Statistics",
                style="standard",
            )
            layout["stats"].update(statistics)
            time.sleep(0.5)
            layout["title"].update(title)
            time.sleep(2)

    def rich_sudoku_grid(self, empty_pos=None):
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
            cols.append(self.grid_numbers(input_num, solved_num, idx, empty_pos))
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

    def grid_numbers(self, input_num, solved_num, idx: int, empty_pos=None):
        # Numbers that are in the input board display in a differnt style
        if idx in self.display_positions:
            if int(input_num):
                style = "input_number"

            else:
                style = "standard"
        else:
            solved_num = empty_pos()
            style = "empty_pos"
        return f"[{style}]{solved_num}[/{style}]"


def get_test_sudokus(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the config file"""
    assert 0 <= puzzle_num < 7, f"Test Sudoku must be 0-6,{puzzle_num} given"
    with open("./data/sudoku_data.json", "r") as f:
        config_data = json.load(f)
    return config_data["sudoku_puzzle"][puzzle_num]["question"]


def list_plugins() -> None:
    print("Available plugins:")
    installed_plugins = plugins.get_plugins()
    for plugin_type in installed_plugins:
        print(f"    {plugin_type}:")
        for plugin in installed_plugins[plugin_type]:
            print(f"        {plugin}")


def parse_commandline_args():
    parser = argparse.ArgumentParser(
        prog="sudoku", description="Solve any Sudoku puzzle"
    )
    input_parse_group = parser.add_mutually_exclusive_group(required=False)
    input_parse_group.add_argument(
        "-i",
        "--input-board",
        action="store",
        help="use supplied Sudoku string",
        type=str,
    )
    input_parse_group.add_argument(
        "-b",
        "--board-preset",
        help="use preset Sudoku board 1-6",
        action="store",
        choices=range(0, 7),
        type=int,
    )
    parser.add_argument(
        "-p",
        "--plugins",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="0",
    )
    output_parse_group = parser.add_argument_group("Plugins")
    output_parse_group.add_argument(
        "-u",
        "--user-interface",
        help="user interface plugin to use",
        action="store_true",
    )
    output_parse_group.add_argument(
        "-s",
        "--solver",
        help="solver algorithm plugin to use",
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

    # Choose input
    sudoku_input = ""
    if args.plugins:
        list_plugins()
    if args.board_preset is not None:
        sudoku_input = get_test_sudokus(args.board_preset)
    elif args.input_board:
        sudoku_input = args.input_board

    display = ui.SimpleCLI(
        sudoku_input, solver.SudokuSolver, validator.SudokuValidator()
    )
    display.run()


if __name__ == "__main__":
    main()
