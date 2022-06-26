import time

difficulty_score = 0


def display_board(board_list):
    """Prints Sudoku board in readable format"""
    board = "".join(board_list)
    for a in range(0, 81, 27):
        for b in range(0, 27, 9):
            n = a + b

            print(board[n:n+3], " ", board[n+3:n+6], " ", board[n+6:n+9])
        print(" ")


def update_available(i, n, cell_defn):
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


def solve_sudoku(board, rec_depth):
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

    # define the rows, columns, and squares that apply to each cell
    defn_str = """000 010 020   031 041 051   062 072 082
                  100 110 120   131 141 151   162 172 182
                  200 210 220   231 241 251   262 272 282

                  303 313 323   334 344 354   365 375 385
                  403 413 423   434 444 454   465 475 485
                  503 513 523   534 544 554   565 575 585

                  606 616 626   637 647 657   668 678 688
                  706 716 726   737 747 757   768 778 788
                  806 816 826   837 847 857   868 878 888"""
    defn = [(r[int(x)], c[int(y)], s[int(z)]) for x, y, z in defn_str.split()]
    defn = tuple(defn)

    for i, n in enumerate(board):
        update_available(i, n, defn)

    while "0" in board:
        changed = False
        for i, n in enumerate(board):
            if n != "0":
                continue
            available = defn[i][0] & defn[i][1] & defn[i][2]
            if len(available) == 0:
                return False
            if len(available) == 1:
                board[i] = available.pop()
                if "0" not in board:
                    return board
                changed = True
                update_available(i, board[i], defn)
        if changed is False:
            current_lowest = 9
            lowest_pos = 0
            # find position on board with lowest number of alternatives
            for i, n in enumerate(board):
                if n == "0":
                    available = defn[i][0] & defn[i][1] & defn[i][2]
                    if len(available) < current_lowest:
                        current_lowest = len(available)
                        lowest_pos = i
                        lowest_available = available.copy()
            # try each alternative in turn
            for test_num in lowest_available:
                board[lowest_pos] = test_num
                if solved_bd := solve_sudoku(board.copy(), rec_depth+1):
                    return solved_bd
            return False

def main():
    REPS = 20
    global difficulty_score

    solve_time = []
    solve_difficulty = []

    vals = input("Sudoku string: ")

    board_list = clean_string(vals)
    if len(board_list) != 81:
        print("Sudoko board is 81 characters, board has ", len(board_list))
        exit()
    display_board(board_list)
    print("Original board")

    for n in range(REPS):
        new_board_list = board_list.copy()
        t1 = time.time()
        if solved_board := solve_sudoku(new_board_list, 0):
            t2 = time.time()
            solve_time.append(t2-t1)
            solve_difficulty.append(difficulty_score)
            difficulty_score = 0

        else:
            print("Too hard")

    print("\n\nSolved Board\n")
    display_board(solved_board)
    print("".join(solved_board))
    print("Execution time = ", sum(solve_time) / len(solve_time))
    print("Diffulty = ", sum(solve_difficulty) / len(solve_difficulty))


if __name__ == "__main__":
    main()
