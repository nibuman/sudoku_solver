from sudoku_solver.ui import api
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


class UserInterface(api.ABCUI):
    ALL_POSITIONS = set(range(81))
    theme = Theme(
        {
            "input_number": "bold red on white",
            "standard": "bold black on white",
            "data": "blue on white",
            "title": "underline black on white",
            "empty_pos": "grey50 on white",
        }
    )

    def run(self):
        self.solved_boards = self.solver.solve_sudoku(
            self.input_board, 1, self.validator.validate_solved_board
        )
        self._display_board()

    def _get_input(self) -> str:
        return input("Enter Sudoku board:")

    def _display_board(self) -> None:
        """Display a formatted Sudoku board in the terminal using the rich library"""
        console = Console(theme=self.theme, height=18, width=30, style="standard")
        layout = Layout()

        # Title
        title = Align("[title]Sudoku Solver[/title]", align="center")

        # Sudoku grid
        self.display_positions = self.ALL_POSITIONS
        grid = self.rich_sudoku_grid()

        # Statistics panel
        statistics = Panel(
            f"Speed: [data]{1000*(0):5.1f} [standard]ms\n"
            f"Difficulty: [data]{0}[/data]",
            title="Statistics",
        )

        layout.split_column(
            Layout(title, name="title", size=1),
            Layout(grid, name="grid", size=13),
            Layout(statistics, name="stats", size=4),
        )
        console.print(layout)

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
            zip(self.input_board, self.solved_boards[0])
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

    def grid_numbers(self, input_num, solved_num, idx: int, empty_pos=" "):
        # Numbers that are in the input board display in a differnt style
        if idx in self.display_positions:
            if int(input_num):
                style = "input_number"

            else:
                style = "standard"
        else:
            solved_num = empty_pos
            style = "empty_pos"
        return f"[{style}]{solved_num}[/{style}]"

    def add_rows_to_grid(self, grid: Table, sqr):
        grid.add_row(
            Align(sqr[0], align="center"),
            Align(sqr[1], align="center"),
            Align(sqr[2], align="center"),
            style="standard",
        )
