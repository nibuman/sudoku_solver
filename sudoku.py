__version__ = "1.2"

import time

difficulty_score = 0


def display_board(board_list: list) -> None:
    """Prints Sudoku board in readable format"""
    board = "".join(board_list)
    for a in range(0, 81, 27):
        for b in range(0, 27, 9):
            n = a + b

            print(board[n:n+3], " ", board[n+3:n+6], " ", board[n+6:n+9])
        print(" ")


def update_available(i: int, n: str, cell_defn: tuple) -> None:
    """Update rows, columns and squares by removing unavailable numbers"""
    for j in range(3):
        cell_defn[i][j].discard(n)


def clean_string(board_string):
    """Reformats a text string as a valid board definition

    - will remove any characters that are not 0-9
    """
    allowed_vals = {str(n) for n in range(10)}
    board_list = [n for n in board_string if n in allowed_vals]
    return board_list


def solve_sudoku(board: list, rec_depth: int, use_alg2: bool = True) -> list:
    """Try to solve any Sudoku board, needs to be called for each guess

    - Iterates through every cell
    - Removes any values already used in each row, column or square
    - If only one value possible for a cell - then assign that
    - If no previous iterations don't find any valid values then:
    - Try different values
    """
    global difficulty_score
    difficulty_score += 1

    # lists of sets of available numbers by row, column or square
    r = [{str(n) for n in range(1, 10)} for _ in range(9)]
    c = [{str(n) for n in range(1, 10)} for _ in range(9)]
    s = [{str(n) for n in range(1, 10)} for _ in range(9)]
    r1 = [[[] for _ in range(10)] for _ in range(9)]
    c1 = [[[] for _ in range(10)] for _ in range(9)]
    s1 = [[[] for _ in range(10)] for _ in range(9)]

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
    # format string as (({row}, {col}, {sq}, [r1], [c1], [s1]),...)
    defn = [(r[int(x)], c[int(y)], s[int(z)],
            r1[int(x)], c1[int(y)], s1[int(z)])
            for x, y, z in defn_str.split()]
    defn = tuple(defn)

    for i, n in enumerate(board):
        update_available(i, n, defn)

    while "0" in board:
        for i in range(9):
            for j in range(10):
                r1[i][j].clear()
                c1[i][j].clear()
                s1[i][j].clear()
        changed = False
        lowest = {"position": 0, "count": 9, "values": {}}
        for i, n in enumerate(board):
            if n != "0":
                continue
            # looking for positions where there is only one availble
            # value left (because the others are in the same row,
            # column, or square)
            available = defn[i][0] & defn[i][1] & defn[i][2]
            available_count = len(available)
            for number in available:
                defn[i][3][int(number)].append(i)
                defn[i][4][int(number)].append(i)
                defn[i][5][int(number)].append(i)
            if available_count == 0:  # must be an invalid board
                return False
            if available_count == 1:  # must be that number in this position
                board[i] = available.pop()
                if "0" not in board:
                    return board
                changed = True
                update_available(i, board[i], defn)
            elif available_count < lowest["count"]:
                lowest["count"] = available_count
                lowest["position"] = i
                lowest["values"] = available.copy()
        # run the second algorithm - each row, col, sq must have 1 of
        # all 9 numbers. Cannot run if there have been changes made as
        # r1, c1, and s1 will not be up-to-date
        if changed is False and use_alg2 is True:
            for row in (r1 + c1 + s1):
                for pos, available_pos in enumerate(row):
                    if len(available_pos) == 1:
                        board[available_pos[0]] = str(pos)
                        if "0" not in board:
                            return board
                        changed = True
                        update_available(available_pos[0], str(pos), defn)

        if changed is False:
            # try each possible alternative value in turn
            # using the board position with fewest alternatives
            # to reduce the amount of recursion
            for test_num in lowest["values"]:
                board[lowest["position"]] = test_num
                if solved_bd := solve_sudoku(board.copy(), rec_depth+1, use_alg2):
                    return solved_bd
            return False


def main():
    global difficulty_score

    sudoku_input = input("Sudoku string: ")
    board_list = clean_string(sudoku_input)
    if len(board_list) != 81:
        print("Sudoko board is 81 characters, board has ", len(board_list))
        exit()
    print("Original board")
    display_board(board_list)

    t1 = time.time()
    if solved_board := solve_sudoku(board_list, 0, False):
        t2 = time.time()
    else:
        print("Too hard")
    print("Solved board")
    display_board(solved_board)
    print(f'Solved in {t2-t1:8.5f} ms with difficulty {difficulty_score}')


if __name__ == "__main__":
    main()
