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


def string_to_board_list(board_string):
    """Reformats a text string as a valid board definition

    - will remove any characters that are not 0-9
    """
    allowed_vals = {str(n) for n in range(10)}
    board_list = [n for n in board_string if n in allowed_vals]
    if len(board_list) != 81:
        print("Sudoko board is 81 characters, board has ", len(board_list))
        exit()
    return board_list


def solve_sudoku(board, rec_depth):
    """Try to solve any Sudoku board, needs to called for each guess

    - Iterates through every cell
    - Removes any values already used in each row, column or square
    - If only one value possible for a cell - then assign that
    - If no previous iterations don't find any valid values then:
    - Try different values
    """
    global difficulty_score
    difficulty_score += 1
    print(rec_depth)
    # lists of sets of available numbers by row, column or square
    r = [{str(n) for n in range(1, 10)} for _ in range(9)]
    c = [{str(n) for n in range(1, 10)} for _ in range(9)]
    s = [{str(n) for n in range(1, 10)} for _ in range(9)]

    # define the rows, columns, and squares that apply to each cell
    defn = [[r[0], c[0], s[0]], [r[0], c[1], s[0]], [r[0], c[2], s[0]], [r[0], c[3], s[1]], [r[0], c[4], s[1]], [r[0], c[5], s[1]], [r[0], c[6], s[2]], [r[0], c[7], s[2]], [r[0], c[8], s[2]],
            [r[1], c[0], s[0]], [r[1], c[1], s[0]], [r[1], c[2], s[0]], [r[1], c[3], s[1]], [r[1], c[4], s[1]], [r[1], c[5], s[1]], [r[1], c[6], s[2]], [r[1], c[7], s[2]], [r[1], c[8], s[2]],
            [r[2], c[0], s[0]], [r[2], c[1], s[0]], [r[2], c[2], s[0]], [r[2], c[3], s[1]], [r[2], c[4], s[1]], [r[2], c[5], s[1]], [r[2], c[6], s[2]], [r[2], c[7], s[2]], [r[2], c[8], s[2]],
            [r[3], c[0], s[3]], [r[3], c[1], s[3]], [r[3], c[2], s[3]], [r[3], c[3], s[4]], [r[3], c[4], s[4]], [r[3], c[5], s[4]], [r[3], c[6], s[5]], [r[3], c[7], s[5]], [r[3], c[8], s[5]],
            [r[4], c[0], s[3]], [r[4], c[1], s[3]], [r[4], c[2], s[3]], [r[4], c[3], s[4]], [r[4], c[4], s[4]], [r[4], c[5], s[4]], [r[4], c[6], s[5]], [r[4], c[7], s[5]], [r[4], c[8], s[5]],
            [r[5], c[0], s[3]], [r[5], c[1], s[3]], [r[5], c[2], s[3]], [r[5], c[3], s[4]], [r[5], c[4], s[4]], [r[5], c[5], s[4]], [r[5], c[6], s[5]], [r[5], c[7], s[5]], [r[5], c[8], s[5]],
            [r[6], c[0], s[6]], [r[6], c[1], s[6]], [r[6], c[2], s[6]], [r[6], c[3], s[7]], [r[6], c[4], s[7]], [r[6], c[5], s[7]], [r[6], c[6], s[8]], [r[6], c[7], s[8]], [r[6], c[8], s[8]],
            [r[7], c[0], s[6]], [r[7], c[1], s[6]], [r[7], c[2], s[6]], [r[7], c[3], s[7]], [r[7], c[4], s[7]], [r[7], c[5], s[7]], [r[7], c[6], s[8]], [r[7], c[7], s[8]], [r[7], c[8], s[8]],
            [r[8], c[0], s[6]], [r[8], c[1], s[6]], [r[8], c[2], s[6]], [r[8], c[3], s[7]], [r[8], c[4], s[7]], [r[8], c[5], s[7]], [r[8], c[6], s[8]], [r[8], c[7], s[8]], [r[8], c[8], s[8]]]

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
                    display_board(board)
                    return True
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
                if solve_sudoku(board.copy(), rec_depth+1):
                    return True
            return False


REPS = 20
solve_time = []
solve_difficulty = []

vals = input("Sudoku string: ")

board_list = string_to_board_list(vals)
display_board(board_list)
print("Original board")
for n in range(REPS):
    new_board_list = board_list.copy()
    t1 = time.time()
    if solve_sudoku(new_board_list, 0):
        print("Solved...", n+1)
        t2 = time.time()
        solve_time.append(t2-t1)
        solve_difficulty.append(difficulty_score)
        difficulty_score = 0

    else:
        print("Too hard")


print("Execution time = ", sum(solve_time) / len(solve_time))
print("Diffulty = ", sum(solve_difficulty) / len(solve_difficulty))
