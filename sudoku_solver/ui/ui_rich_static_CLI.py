from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout

from sudoku_solver.ui import rich_functions

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
    _display_board(cleaned_input_board, solved_boards[0])


def _clean_and_validate(input_board: str, validator) -> str:
    cleaned_input_board = validator.clean_string(input_board)
    if not validator.validate_input_board(cleaned_input_board):
        raise ValueError("Input board not valid")
    return cleaned_input_board


def _get_input() -> str:
    return input("Enter Sudoku board:")


def _display_board(input_board, solved_board) -> None:
    console = Console(theme=theme, height=18, width=30, style="standard")
    layout = Layout()

    # Title
    title = Align("[title]Sudoku Solver[/title]", align="center")

    # Sudoku grid

    grid = rich_functions.rich_sudoku_grid(
        input_board, solved_board, rich_functions.ALL_POSITIONS
    )

    # Statistics panel
    statistics = Panel(
        f"Speed: [data]{1000*(0):5.1f} [standard]ms\n" f"Difficulty: [data]{0}[/data]",
        title="Statistics",
    )

    layout.split_column(
        Layout(title, name="title", size=1),
        Layout(grid, name="grid", size=13),
        Layout(statistics, name="stats", size=4),
    )
    console.print(layout)
