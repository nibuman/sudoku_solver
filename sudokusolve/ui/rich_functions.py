from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich import box

ALL_POSITIONS = set(range(81))


def rich_sudoku_grid(
    input_board, solved_board, display_positions, empty_pos_selector=lambda: " "
):
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
    for idx, (input_num, solved_num) in enumerate(zip(input_board, solved_board)):
        if (
            idx % 3 == 0 and idx
        ):  # A space between every 3 numbers (but not before row 0)
            sqr.append(Columns(cols, padding=(0, 1)))
            cols.clear()
        if idx % 9 == 0 and idx:  # Add completed row to grid
            add_rows_to_grid(grid, sqr)
            sqr.clear()
        if idx % 27 == 0 and idx:  # Add a line (new section) after every 3 rows
            grid.add_section()
        cols.append(
            grid_numbers(
                input_num, solved_num, display_positions, idx, empty_pos_selector
            )
        )
    # Just need to complete the last row
    sqr.append(Columns(cols, padding=(0, 1)))
    add_rows_to_grid(grid, sqr)
    return grid


def grid_numbers(
    input_num, solved_num, display_positions, idx: int, empty_pos_selector=lambda: " "
):
    # Numbers that are in the input board display in a differnt style
    if idx in display_positions:
        if int(input_num):
            style = "input_number"
        else:
            style = "standard"
    else:
        solved_num = empty_pos_selector()
        style = "empty_pos"
    return f"[{style}]{solved_num}[/{style}]"


def add_rows_to_grid(grid: Table, sqr):
    grid.add_row(
        Align(sqr[0], align="center"),
        Align(sqr[1], align="center"),
        Align(sqr[2], align="center"),
        style="standard",
    )
