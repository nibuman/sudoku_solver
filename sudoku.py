__version__ = "5"

import json
import logging
import time
import argparse
import numpy as np

difficulty_score = 0
quiet = False


class SudokuBoard:
    def __init__(self, board) -> None:
        self.board = board
        self.available_pos_row = [[set() for _ in range(10)] for _ in range(9)]
        self.available_pos_col = [[set() for _ in range(10)] for _ in range(9)]
        self.available_pos_sqr = [[set() for _ in range(10)] for _ in range(9)]

    def get_rcs_alg2(self, position: int) -> tuple:
        """Returns the row, column and square for a particular cell for alg2"""
        r, c = self.get_index(position)
        s = self.get_sqr_index(position)
        return (
            self.available_pos_row[r],
            self.available_pos_col[c],
            self.available_pos_sqr[s],
        )

    def reset_alg2(self):
        """Clears all the available positions used in alg2"""
        for alg2_rcs in (
            self.available_pos_row,
            self.available_pos_col,
            self.available_pos_sqr,
        ):
            for rcs in alg2_rcs:
                for position_set in rcs:
                    position_set.clear()

    def update_alg2(self, position, available):
        alg2_rcs = self.get_rcs_alg2(position)
        for rcs in alg2_rcs:
            for num in available:
                rcs[int(num)].add(position)

    def get_sqr_index(self, position):
        """Returns the number (0-8) of the 3x3 square for given position
        numbered as follows:    0 1 2
                                3 4 5
                                6 7 8
        """
        r, c = self.get_index(position)
        return ((r // 3) * 3) + (c // 3)

    def get_index(self, position):
        """Returns 2d coordinates of position in r,c format"""
        r = position // 9
        c = position % 9
        return (r, c)

    def get_row(self, position: int) -> set:
        """Return set of numbers in row at given position"""
        r, _ = self.get_index(position)
        return set(self.board[r, :])

    def get_col(self, position: int) -> set:
        """Return set of numbers in column at given position"""
        _, c = self.get_index(position)
        return set(self.board[:, c])

    def get_sqr(self, position: int) -> set:
        """Return set of numbers in square at given position"""
        r, c = self.get_index(position)
        sq_row = (r // 3) * 3
        sq_col = (c // 3) * 3
        return set(self.board[sq_row : sq_row + 3, sq_col : sq_col + 3].flatten())

    def get_not_available(self, position: int) -> set:
        """Return set of numbers that are not available in given position"""
        row = self.get_row(position)
        col = self.get_col(position)
        sqr = self.get_sqr(position)
        return set.union(row, col, sqr)

    def get_available(self, position: int) -> set:
        """Return set of numbers that are available in a given position"""
        all_digits = {str(n) for n in range(1, 10)}
        not_available = self.get_not_available(position)
        return all_digits.difference(not_available)

    def update_board(self, position: int, number: str) -> None:
        """Places a number in the board"""
        r, c = self.get_index(position)
        self.board[r, c] = number

    def get_position(self, position: int) -> str:
        """Returns number at given position in board"""
        r, c = self.get_index(position)
        return self.board[r, c]

    def check_valid(self) -> bool:
        """Checks whether sudoku board is valid by definition
        i.e. is there just one of each digit in each row, column and square"""
        if self.board is False:
            return False
        valid_set = {str(n) for n in range(1, 10)}

        # check rows are valid
        for i in range(0, 81, 9):
            if self.get_row(i) != valid_set:
                return False
        # check columns are valid
        for i in range(9):
            if self.get_col(i) != valid_set:
                return False
        # check squares are valid
        for i in range(0, 81, 12):
            if self.get_sqr(i) != valid_set:
                return False
        return self.get_string()

    def display(self) -> None:
        """Prints Sudoku board in readable format"""
        if quiet:
            return
        for a in range(0, 81, 27):
            for b in range(0, 27, 9):
                n = a + b
                r, _ = self.get_index(n)
                row = "".join(self.board[r, :])
                print(row[0:3], " ", row[3:6], " ", row[6:9])
            print("\n")

    def get_string(self) -> str:
        """Returns board as string"""
        return "".join(self.board.flatten())


def valid_string(board_string: str) -> list:
    """Reformats a text string as a valid board definition
    - will remove any characters that are not 0-9
    - Strings starting with 'sud' interpreted as a standard test
      Sudoku from sudoku_test.py numbered 01-99 that it then retrieves
      e.g. sud01 runs the same board as test_sudoku_01
    """
    if board_string[0:3] == "sud":
        board_string = get_test_sudokus(int(board_string[3:5]) - 1)
        logging.info(f"[valid_string]standard test Sudoku {board_string[0:5]}")
    allowed_vals = {str(n) for n in range(10)}
    board_list = [n for n in board_string if n in allowed_vals]
    if len(board_list) != 81:
        return False
    return board_list


def array_from_list(board_list):
    """Returns 1d list as 2d NumPy array"""
    return np.reshape(board_list, (9, 9))


def get_test_sudokus(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the config file"""
    assert 0 <= puzzle_num < 7, f"Test Sudoku must be 01-06,{puzzle_num} given"
    with open("./sudoku_data.json", "r") as f:
        config_data = json.load(f)
    return config_data["sudoku_puzzle"][puzzle_num]["question"]


def alg1(sudoku):
    changed = False
    board_error = False
    lowest = {"position": 0, "count": 9, "values": {}}
    for position, num_str in enumerate(sudoku.board.flatten()):
        if num_str != "0":
            continue
        available = sudoku.get_available(position)
        available_count = len(available)

        if available_count == 0:  # must be an invalid board
            logging.warning(f"[alg1] available_count == 0 in pos {position}")
            board_error = True
            break
        if available_count == 1:  # must be that number in this position
            sudoku.update_board(position, available.pop())
            changed = True
            logging.debug(
                f"[alg1] Assigned {sudoku.get_position(position)}"
                f" to position {position}"
            )
            # sudoku.update_available(position, board[position])
        else:
            if available_count < lowest["count"]:
                lowest["count"] = available_count
                lowest["position"] = position
                lowest["values"] = available.copy()
            sudoku.update_alg2(position, available)

    return {"changed": changed, "error": board_error, "lowest": lowest}


def alg2(sudoku):
    """run the second algorithm - each row, col, sq must have 1 of all 9 numbers"""
    changed = False
    for alg2_rcs in (
        sudoku.available_pos_row,
        sudoku.available_pos_col,
        sudoku.available_pos_sqr,
    ):
        for rcs in alg2_rcs:
            for number, available_pos in enumerate(rcs):
                if len(available_pos) == 1 and number != "0":
                    position = available_pos.pop()
                    sudoku.update_board(position, str(number))
                    logging.debug(
                        f"[alg2] Assigned"
                        f"{sudoku.get_position(position)} to position"
                        f"{position}"
                    )
                    changed = True
    return changed


def alg3(sudoku, lowest):
    """Try each possible alternative value in turn using the board
    position with fewest alternatives to reduce the amount of recursion
    Last resort only runs if cannot fill numbers using other methods.
    """
    for test_num in lowest["values"]:
        sudoku.update_board(lowest["position"], test_num)
        logging.debug(f"[alg3] Trying {test_num}" f'in position {lowest["position"]}')
        if solved_bd := solve_sudoku(list(sudoku.get_string())):
            return solved_bd
    return False


def solve_sudoku(board) -> list:
    """Try to solve any Sudoku board, needs to be called for each guess
    - Iterates through every cell
    - Removes any values already used in each row, column or square
    - If only one value possible for a cell - then assign that
    - If no previous iterations don't find any valid values then:
    - Try different values
    """
    global difficulty_score
    difficulty_score += 1
    sudoku = SudokuBoard(array_from_list(board))
    logging.debug(f"[solve_sudoku] Entering solve_sudoku.")

    while "0" in sudoku.board:
        sudoku.reset_alg2()
        # Alg1
        result = alg1(sudoku)
        if result["error"] is True:
            return False
        if result["changed"] is True:
            continue
        lowest = result["lowest"]

        # Alg 2
        if alg2(sudoku):
            continue

        # Alg 3
        return alg3(sudoku, lowest)

    if result := sudoku.check_valid():
        sudoku.display()
    return result


def main():
    global quiet
    global difficulty_score

    parser = argparse.ArgumentParser(
        prog="sudoku", description="Solve any Sudoku puzzle"
    )
    parse_group = parser.add_mutually_exclusive_group(required=False)
    parse_group.add_argument(
        "-s",
        "--sudoku_string",
        action="store",
        help="use supplied Sudoku string",
        type=str,
    )
    parse_group.add_argument(
        "-p",
        "--preset",
        help="use preset Sudoku board 1-6",
        action="store",
        choices=range(1, 7),
        type=int,
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument(
        "-q", "--quiet", help="display only output string", action="store_true"
    )
    args = parser.parse_args()

    logging.basicConfig(
        filename="sudoku_solver.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )

    logging.info("Started")

    if args.quiet:
        quiet = True
    if args.preset:
        sudoku_input = get_test_sudokus(args.preset)
    elif args.sudoku_string:
        sudoku_input = args.sudoku_string
    else:
        sudoku_input = input("Sudoku string: ")

    if not (board_list := valid_string(sudoku_input)):
        logging.critical("Board string was not valid, exiting")
        exit()
    logging.info(f'Board to solve:{"".join(board_list)}')

    t1 = time.perf_counter()
    if solved_board := solve_sudoku(board_list):
        t2 = time.perf_counter()
        logging.info(f"Board solved in {t2-t1} s")
        logging.info(f"Solution: {solved_board}")

        if quiet:
            print(solved_board)
        else:
            print(
                f"board: {solved_board}\n"
                f"Solved in (ms): {1000*(t2 - t1):5.1f}\n"
                f"difficulty: {difficulty_score}"
            )
    else:
        logging.warning("board: 0")


if __name__ == "__main__":
    main()
