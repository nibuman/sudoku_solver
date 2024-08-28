import itertools
from typing import Callable, Generator

DIGITS_1_TO_9 = {str(n) for n in range(1, 10)}
DIGITS_0_TO_9 = {str(n) for n in range(0, 10)}


def row_gen() -> Generator[tuple[int, ...], None, None]:
    for pos in range(0, 81):
        row_start = (pos // 9) * 9
        yield tuple(range(row_start, row_start + 9))


def col_gen() -> Generator[tuple[int, ...], None, None]:
    for pos in range(81):
        col = pos % 9
        yield tuple(col + n for n in range(0, 81, 9))


def sqr_gen() -> Generator[tuple[int, ...], None, None]:
    for pos in range(81):
        r = (pos // 27) * 27
        c = ((pos // 3) % 3) * 3
        offsets = (0, 1, 2, 9, 10, 11, 18, 19, 20)
        yield tuple(r + c + o for o in offsets)


RCS_POSITIONS = tuple(zip(row_gen(), col_gen(), sqr_gen()))
ROW_POSITIONS = tuple(itertools.islice(row_gen(), 0, 81, 9))
COL_POSITIONS = tuple(itertools.islice(col_gen(), 9))
SQR_POSITIONS = tuple(
    sqr for i, sqr in enumerate(sqr_gen()) if i in (0, 3, 6, 27, 30, 33, 54, 57, 60)
)
PHISTOMEFAL_POSITIONS = (
    (0, 1, 9, 10, 7, 8, 16, 17, 63, 64, 72, 73, 70, 71, 79, 80),
    (20, 21, 22, 23, 24, 29, 33, 38, 42, 47, 51, 56, 57, 58, 59, 60),
)


def phistomefel_ring_gen(): ...


def unknown_positions_gen(board):
    for num in board:
        yield num == "0"


def available_number_gen(board):
    for idx, number in enumerate(board):
        if number == "0":
            rcs = {board[n] for n in itertools.chain(*RCS_POSITIONS[idx]) if n != "0"}
            yield DIGITS_1_TO_9.difference(rcs)
        else:
            yield {number}


def only_number_in_position_gen(board):
    for idx, numbers in itertools.compress(
        enumerate(available_number_gen(board)), unknown_positions_gen(board)
    ):
        if len(numbers) == 1:
            yield idx, numbers.pop()


def only_position_in_rcs_gen(board):
    available_numbers = tuple(available_number_gen(board))
    unknown_positions = tuple(unknown_positions_gen(board))
    for rcs in itertools.chain(ROW_POSITIONS, COL_POSITIONS, SQR_POSITIONS):
        positions_for_each_number = {d: [] for d in DIGITS_1_TO_9}
        for pos in rcs:
            for num in available_numbers[pos]:
                positions_for_each_number[num].append(pos)
        for num, positions in positions_for_each_number.items():
            if len(positions) == 1 and unknown_positions[positions[0]]:
                yield positions.pop(), num


def substitute_board(board, substitutions: dict[int, str]):
    for idx, num in enumerate(board):
        if idx in substitutions:
            yield substitutions[idx]
        else:
            yield num


def solve_sudoku(
    board, completed_board_validator: Callable[[str], bool], max_solutions: int = 1
):
    boards = []
    solved_boards = []
    while True:
        only_possible_numbers = {i: n for i, n in only_number_in_position_gen(board)}
        only_position_in_rcs = {i: n for i, n in only_position_in_rcs_gen(board)}
        substitutions = only_possible_numbers | only_position_in_rcs
        if substitutions:
            board = "".join(substitute_board(board, substitutions))
        elif not any(unknown_positions_gen(board)) and completed_board_validator(board):
            solved_boards.append(board)
            if len(solved_boards) >= max_solutions:
                break
            try:
                board = boards.pop()
            except IndexError:
                break
        else:
            try:
                pos, numbers = min(
                    filter(
                        lambda x: len(x[1]) > 1, enumerate(available_number_gen(board))
                    ),
                    key=lambda x: len(x[1]),
                )
            except ValueError:
                try:
                    board = boards.pop()
                    continue
                except IndexError:
                    break
            substitions = [{pos: n} for n in numbers]
            boards.extend(
                "".join(substitute_board(board, subs)) for subs in substitions
            )
            board = boards.pop()
    return solved_boards
