import random
import time

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.theme import Theme

from sudokusolve.ui import rich_functions

theme = Theme(
    {
        "input_number": "bold red on white",
        "standard": "bold black on white",
        "data": "blue on white",
        "title": "underline black on white",
        "empty_pos": "grey50 on white",
    }
)


def run(input_board: str | None, solver, validator, max_solutions: int = 1):
    if not input_board:
        input_board = _get_input()
    cleaned_input_board = _clean_and_validate(input_board, validator)
    solved_boards = solver.solve_sudoku(
        cleaned_input_board, validator.validate_solved_board, max_solutions
    )
    _display_animated(cleaned_input_board, solved_boards[0])


def _clean_and_validate(input_board: str, validator) -> str:
    cleaned_input_board = validator.clean_string(input_board)
    if not validator.validate_input_board(cleaned_input_board):
        raise ValueError("Input board not valid")
    return cleaned_input_board


def _get_input() -> str:
    return input("Enter Sudoku board:")


def _display_animated(input_board, solved_board) -> None:
    """Display a formatted Sudoku board in the terminal using the rich library"""
    console = Console(theme=theme, height=18, width=28, style="standard")
    layout = Layout()

    # Title
    title = Align("[title]Sudoku Solver[/title]", align="center", style="standard")

    # Sudoku grid
    display_positions = {idx for idx, num in enumerate(input_board) if int(num)}
    remaining_positions = rich_functions.ALL_POSITIONS.difference(display_positions)
    grid = rich_functions.rich_sudoku_grid(
        input_board, solved_board, display_positions, lambda: " "
    )
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
        title = Align("[title]Sudoku Solved[/title]", align="center", style="standard")
        while remaining_positions:
            next_pos = random.choice(list(remaining_positions))
            remaining_positions.discard(next_pos)
            display_positions.add(next_pos)
            grid = rich_functions.rich_sudoku_grid(
                input_board,
                solved_board,
                display_positions,
                empty_pos_selector=lambda: str(random.choice(list(range(1, 10)))),
            )
            layout["grid"].update(grid)
            time.sleep(0.05)

            # Statistics panel
        statistics = Panel(
            f"[standard]Speed: [data]{1000*(1):5.1f} [standard]ms\n"
            f"[standard]Difficulty: [data]{1}[/data]",
            title="Statistics",
            style="standard",
        )
        layout["stats"].update(statistics)
        time.sleep(0.5)
        layout["title"].update(title)
        time.sleep(2)
