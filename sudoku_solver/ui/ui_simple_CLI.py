from sudoku_solver.ui import uis


class SimpleCLI(uis.ABCUI):
    def __init__(self, input_board: str | None, Solver, validator) -> None:
        self.validator = validator
        self.input_board = input_board
        self.solver = Solver(self.input_board)

    @property
    def input_board(self):
        return self._board

    @input_board.setter
    def input_board(self, value):
        if not value:
            value = self.get_input()
        cleaned_board = self.validator.clean_string(value)
        if self.validator.validate_input_board(cleaned_board):
            self._board = cleaned_board
        else:
            raise ValueError

    def run(self):
        print("Input board:")
        self.display_plain(self.input_board)
        self.solved_boards = self.solver.solve_sudoku()
        print("Solved board:")
        self.display_plain(self.solved_boards[0])

    def get_input(self) -> str:
        return input("Enter Sudoku board:")

    def display_plain(self, board) -> None:
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
