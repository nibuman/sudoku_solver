from sudoku_solver.ui import api


class UserInterface(api.ABCUI):
    def run(self):
        print("Input board:")
        self._display_board(self.input_board)
        self.solved_boards = self.solver.solve_sudoku(
            self.input_board, 1, self.validator.validate_solved_board
        )
        print("Solved board:")
        self._display_board(self.solved_boards[0])

    def _get_input(self) -> str:
        return input("Enter Sudoku board:")

    def _display_board(self, board) -> None:
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
