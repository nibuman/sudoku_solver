__version__ = "4"

import copy
import json
import logging
import time

difficulty_score = 0


class BoardDefinition():

    def __init__(self) -> None:
        # lists of sets of available numbers by row, column or square
        self.r = [{str(n) for n in range(1, 10)} for _ in range(9)]
        self.c = copy.deepcopy(self.r)
        self.s = copy.deepcopy(self.r)
        self.alg2_r = [[set() for _ in range(10)] for _ in range(9)]
        self.alg2_c = copy.deepcopy(self.alg2_r)
        self.alg2_s = copy.deepcopy(self.alg2_r)

        # define which rows, columns, and squares apply to each cell
        defn_str = """000 010 020   031 041 051   062 072 082
                    100 110 120   131 141 151   162 172 182
                    200 210 220   231 241 251   262 272 282

                    303 313 323   334 344 354   365 375 385
                    403 413 423   434 444 454   465 475 485
                    503 513 523   534 544 554   565 575 585

                    606 616 626   637 647 657   668 678 688
                    706 716 726   737 747 757   768 778 788
                    806 816 826   837 847 857   868 878 888"""
        # format string as (({row}, {col}, {sq}, [alg2_r1], [alg2_c1],...)
        self.defn = tuple(
                            [(self.r[int(x)],
                              self.c[int(y)],
                              self.s[int(z)],
                              self.alg2_r[int(x)],
                              self.alg2_c[int(y)],
                              self.alg2_s[int(z)])
                             for x, y, z in defn_str.split()]
                          )

    def get_rcs_alg1(self, cell: int) -> tuple:
        """Returns the row, column and square for a particular cell
        """
        alg1_rcs = [self.defn[cell][rcs] for rcs in range(3)]
        return tuple(alg1_rcs)

    def get_rcs_alg2(self, cell: int) -> tuple:
        """Returns the row, column and square for a particular cell
           for alg2
        """
        alg2_rcs = [self.defn[cell][rcs] for rcs in range(3, 6)]
        return tuple(alg2_rcs)

    def initialise_available(self, board: list) -> list:
        """ Move to BoardDefinition Class????"""
        for position, number in enumerate(board):
            self.update_available(position, number)

        for position, number in enumerate(board):
            if number != "0":
                continue

    def reset_alg2(self):
        for alg2_rcs in (self.alg2_r,
                         self.alg2_c,
                         self.alg2_s):
            for rcs in alg2_rcs:
                for position_set in rcs:
                    position_set.clear()

    def get_available(self, position: int) -> set:
        """Return numbers that are available in a given position
        """
        row, col, sqr = self.get_rcs_alg1(position)
        return row & col & sqr

    def update_available(self,
                         board_pos: int,
                         number: str) -> None:
        """Update rows, columns and squares by removing unavailable numbers
        """
        for rcs in self.get_rcs_alg1(board_pos):
            rcs.discard(number)


def display_board(board_list: list) -> None:
    """Prints Sudoku board in readable format"""
    board = "".join(board_list)
    for a in range(0, 81, 27):
        for b in range(0, 27, 9):
            n = a + b
            print(board[n:n+3], " ", board[n+3:n+6], " ", board[n+6:n+9])
        print("\n")


def valid_string(board_string: str) -> list:
    """Reformats a text string as a valid board definition
    - will remove any characters that are not 0-9
    - Strings starting with 'sud' interpreted as a standard test
      Sudoku from sudoku_test.py numbered 01-99 that it then retrieves
      e.g. sud01 runs the same board as test_sudoku_01
    """
    if board_string[0:3] == "sud":
        board_string = get_test_sudokus(int(board_string[3:5])-1)
        logging.info(f'[valid_string]standard test Sudoku {board_string[0:5]}')
    allowed_vals = {str(n) for n in range(10)}
    board_list = [n for n in board_string if n in allowed_vals]
    if len(board_list) != 81:
        return False
    return board_list


def get_test_sudokus(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the config file
    """
    assert 0 <= puzzle_num < 7, f'Test Sudoku must be 01-07,{puzzle_num} given'
    with open('./sudoku_data.json', 'r') as f:
        config_data = json.load(f)
    return config_data["sudoku_puzzle"][puzzle_num]["question"]


def check_valid_sudoku(board: list) -> bool:
    """ Checks whether sudoku board is valid by definition
    i.e. is there just one of each digit in each row, column
    and square
    """
    if board is False:
        return False
    valid_set = {str(n) for n in range(1, 10)}

    # check rows are valid
    for i in range(0, 81, 9):
        row = set(board[i:i+9])
        if row != valid_set:
            return False
    # check columns are valid
    for i in range(9):
        col = set(board[i::9])
        if col != valid_set:
            return False
    # check squares are valid
    for i in range(0, 81, 27):
        for j in range(0, 9, 3):
            sq = []
            for k in range(0, 27, 9):
                sq.extend(board[i+j+k:i+j+k+3])
            sq = set(sq)
            if sq != valid_set:
                return False
    return board


def alg1(board, board_def):
    changed = False
    board_error = False
    lowest = {"position": 0, "count": 9, "values": {}}
    for position, num_str in enumerate(board):
        if num_str != "0":
            continue
        available = board_def.get_available(position)
        available_count = len(available)

        if available_count == 0:  # must be an invalid board
            logging.warning(f'[alg1] available_count == 0 in pos {position}')
            board_error = True
            break
        if available_count == 1:  # must be that number in this position
            board[position] = available.pop()
            changed = True
            logging.debug(f'[alg1] Assigned {board[position]}'
                          f' to position {position}')
            board_def.update_available(position, board[position])
        else:
            if available_count < lowest["count"]:
                lowest["count"] = available_count
                lowest["position"] = position
                lowest["values"] = available.copy()
            update_alg2(available, board_def, position)

    return {'changed': changed, 'error': board_error, 'lowest': lowest}


def update_alg2(available: set, board_def: list, position: int) -> None:
    """Updates the list of sets of available positions for each number
    in a row, column, or square
    """
    alg2_rcs = board_def.get_rcs_alg2(position)
    for number in available:
        for rcs in alg2_rcs:
            rcs[int(number)].add(position)


def alg2(board, board_def):
    """run the second algorithm - each row, col, sq must have 1 of all 9 numbers.
    """
    changed = False
    for alg2_rcs in (board_def.alg2_r,
                     board_def.alg2_c,
                     board_def.alg2_s):
        for rcs in alg2_rcs:
            for number, available_pos in enumerate(rcs):
                if len(available_pos) == 1:
                    position = available_pos.pop()
                    board[position] = str(number)
                    logging.debug(f'[alg2] Assigned'
                                  f'{board[position]} to position'
                                  f'{position}')
                    changed = True
                    board_def.update_available(board_pos=position,
                                               number=str(number))

    return changed


def alg3(board, board_def, lowest, use_alg2):
    """Try each possible alternative value in turn using the board
    position with fewest alternatives to reduce the amount of recursion
    Last resort only runs if cannot fill numbers using other methods.
    """
    for test_num in lowest["values"]:
        board[lowest["position"]] = test_num
        logging.debug(f'[alg3] board object {id(board)}')
        logging.debug(f'[alg3] Trying {test_num}'
                      f'in position {lowest["position"]}')
        if solved_bd := solve_sudoku(board.copy(), use_alg2):
            return solved_bd
    return False


def solve_sudoku(board: list, use_alg2: bool = True) -> list:
    """Try to solve any Sudoku board, needs to be called for each guess
    - Iterates through every cell
    - Removes any values already used in each row, column or square
    - If only one value possible for a cell - then assign that
    - If no previous iterations don't find any valid values then:
    - Try different values
    """
    global difficulty_score
    difficulty_score += 1
    board_def = BoardDefinition()
    logging.debug(f'[solve_sudoku] Entering solve_sudoku. Alg2={use_alg2}')
    board_def.initialise_available(board)

    while "0" in board:
        board_def.reset_alg2()
        # Alg1
        result = alg1(board, board_def)
        if result['error'] is True:
            return False
        if result['changed'] is True:
            continue
        lowest = result['lowest']

        # Alg 2
        if use_alg2:
            if alg2(board, board_def):
                continue

        # Alg 3
        return alg3(board, board_def, lowest, use_alg2)

    return check_valid_sudoku(board)


def main():
    logging.basicConfig(filename='sudoku_solver.log',
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.ERROR)
    logging.info("Started")
    global difficulty_score

    sudoku_input = input("Sudoku string: ")

    if not(board_list := valid_string(sudoku_input)):
        print("Not a valid Sudoku board")
        logging.critical("Board string was not valid, exiting")
        exit()
    print("Original board")
    display_board(board_list)
    logging.info(f'Board to solve:{"".join(board_list)}')
    t1 = time.time()
    if solved_board := solve_sudoku(board_list, use_alg2=True):
        t2 = time.time()
        logging.info(f'Board solved in {t2-t1} s')
        logging.info(f'Solution: {"".join(solved_board)}')
        display_board(solved_board)
        print(f'{"".join(solved_board)}\n'
              f'Solved in {1000*(t2 - t1):5.1f} ms, '
              f'difficulty {difficulty_score}')
    else:
        print("Too hard")
        logging.warning("Board could not be solved")


if __name__ == "__main__":
    main()
