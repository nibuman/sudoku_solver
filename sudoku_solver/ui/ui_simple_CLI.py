MAX_BOARDS_TO_DISPLAY = 5


def run(input_board: str | None, solver, validator, max_solutions: int = 1):
    if not input_board:
        input_board = _get_input()
    cleaned_input_board = _clean_and_validate(input_board, validator)
    print("Input board:")
    _display_board(cleaned_input_board)
    solved_boards = solver.solve_sudoku(
        cleaned_input_board, max_solutions, validator.validate_solved_board
    )
    _display_all_solutions(solved_boards)


def _clean_and_validate(input_board: str, validator) -> str:
    cleaned_input_board = validator.clean_string(input_board)
    if not validator.validate_input_board(cleaned_input_board):
        raise ValueError("Input board not valid")
    return cleaned_input_board


def _display_all_solutions(solved_boards: list[str]) -> None:
    number_of_solutions = len(solved_boards)
    for idx, board in enumerate(solved_boards):
        if idx == min([MAX_BOARDS_TO_DISPLAY, number_of_solutions]):
            break
        print(f"Solved board {idx + 1}:")
        _display_board(board)


def _get_input() -> str:
    return input("Enter Sudoku board:")


def _display_board(board) -> None:
    """Display plain text Sudoku board in terminal"""
    output = ""
    for idx, num in enumerate(board):
        if idx % 27 == 0 and idx:  # Blank line after every 3 rows (not before row 0)
            output += "\n\n"
        elif idx % 9 == 0 and idx:  # Newline at end of every row (not before row 0)
            output += "\n"
        elif idx % 3 == 0 and idx:  # A space between every 3 numbers (not before row 0)
            output += " "
        output += num
    output += "\n"
    print(output)
