import logging

MAX_BOARDS_TO_DISPLAY = 5


def run(input_board: str | None, solver, validator, max_solutions: int = 1):
    if not input_board:
        raise ValueError("This UI needs to be supplied with a valid board")
    cleaned_input_board = _clean_and_validate(input_board, validator)
    solved_boards = solver.solve_sudoku(
        cleaned_input_board, validator.validate_solved_board, max_solutions
    )
    logging.info(f"{solved_boards=}")
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
        _display_board(board)


def _display_board(board) -> None:
    """Display plain text Sudoku board in terminal"""
    print(board)
