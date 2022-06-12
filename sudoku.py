def display_board(board_list):
	board = "".join(board_list)
	for a in range(0, 81, 27):
		for b in range(0, 27, 9):
			n  = a + b
			print(board[n:n+3], " ", board[n+3:n+6], " ", board[n+6:n+9])
		print(" ")
	
def update_available(i, n, cell_defn):
	for j in range(3):	
		cell_defn[i][j].discard(n)

def string_to_board_list(board_string):
	allowed_vals = {str(n) for n in range(10)}
	board_list = [n for n in board_string if n in allowed_vals]
	if len(board_list) != 81:
		print("Sudoko board should be 81 characters, this board has ", len(board_list))
		exit()
	return board_list

def solve_sudoku(board, rec_depth):
	print(rec_depth)
	r = [{str(n) for n in range(1,10)} for i in range(9)] #list of sets of available numbers for each row
	c = [{str(n) for n in range(1,10)} for i in range(9)] #list of sets of available numbers for each column
	s = [{str(n) for n in range(1,10)} for i in range(9)] #list of sets of available numbers for each square
	
	#define the rows, columns, and squares that apply to each cell in the board
	defn = [[r[0], c[0], s[0]], [r[0], c[1], s[0]], [r[0], c[2], s[0]], [r[0], c[3], s[1]], [r[0], c[4], s[1]], [r[0], c[5], s[1]], [r[0], c[6], s[2]], [r[0], c[7], s[2]], [r[0], c[8], s[2]], \
				[r[1], c[0], s[0]], [r[1], c[1], s[0]], [r[1], c[2], s[0]], [r[1], c[3], s[1]], [r[1], c[4], s[1]], [r[1], c[5], s[1]], [r[1], c[6], s[2]], [r[1], c[7], s[2]], [r[1], c[8], s[2]],\
				[r[2], c[0], s[0]], [r[2], c[1], s[0]], [r[2], c[2], s[0]], [r[2], c[3], s[1]], [r[2], c[4], s[1]], [r[2], c[5], s[1]], [r[2], c[6], s[2]], [r[2], c[7], s[2]], [r[2], c[8], s[2]], \
				[r[3], c[0], s[3]], [r[3], c[1], s[3]], [r[3], c[2], s[3]], [r[3], c[3], s[4]], [r[3], c[4], s[4]], [r[3], c[5], s[4]], [r[3], c[6], s[5]], [r[3], c[7], s[5]], [r[3], c[8], s[5]], \
				[r[4], c[0], s[3]], [r[4], c[1], s[3]], [r[4], c[2], s[3]], [r[4], c[3], s[4]], [r[4], c[4], s[4]], [r[4], c[5], s[4]], [r[4], c[6], s[5]], [r[4], c[7], s[5]], [r[4], c[8], s[5]], \
				[r[5], c[0], s[3]], [r[5], c[1], s[3]], [r[5], c[2], s[3]], [r[5], c[3], s[4]], [r[5], c[4], s[4]], [r[5], c[5], s[4]], [r[5], c[6], s[5]], [r[5], c[7], s[5]], [r[5], c[8], s[5]], \
				[r[6], c[0], s[6]], [r[6], c[1], s[6]], [r[6], c[2], s[6]], [r[6], c[3], s[7]], [r[6], c[4], s[7]], [r[6], c[5], s[7]], [r[6], c[6], s[8]], [r[6], c[7], s[8]], [r[6], c[8], s[8]], \
				[r[7], c[0], s[6]], [r[7], c[1], s[6]], [r[7], c[2], s[6]], [r[7], c[3], s[7]], [r[7], c[4], s[7]], [r[7], c[5], s[7]], [r[7], c[6], s[8]], [r[7], c[7], s[8]], [r[7], c[8], s[8]], \
				[r[8], c[0], s[6]], [r[8], c[1], s[6]], [r[8], c[2], s[6]], [r[8], c[3], s[7]], [r[8], c[4], s[7]], [r[8], c[5], s[7]], [r[8], c[6], s[8]], [r[8], c[7], s[8]], [r[8], c[8], s[8]]]

	for i, n in enumerate(board):
		update_available(i, n, defn)

	while "0" in board:
		changed = False
		for i,n in enumerate(board):
			if n == "0":
				available = defn[i][0] & defn[i][1] & defn[i][2]
				if len(available) == 0:
					return False
				if len(available) == 1:
					board[i] = available.pop()
					if not "0" in board:
						display_board(board)
						return True
					changed = True
					update_available(i, board[i], defn)
		if changed == False:
			current_lowest = 9
			lowest_pos = 0
			#find position on board with lowest number of alternatives
			for i,n in enumerate(board):
				if n == "0":
					available = defn[i][0] & defn[i][1] & defn[i][2]
					if len(available) < current_lowest:
						current_lowest = len(available)
						lowest_pos = i
						lowest_available = available.copy()
			#try each alternative in turn
			for test_num in lowest_available:
				board[lowest_pos] = test_num
				if solve_sudoku(board.copy(), rec_depth+1):
					return True
			return False
			
#vals = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
#vals = "005306078200407005000009106008002034040030010130700500709800000800604001450203600"
#vals = "069800500000000103400000020000170000080006000307020004000040200630000000850000000"
#vals = "006080300049070250000405000600317004007000800100826009000702000075040190003090600"
#vals = "300200000000107000706030500070009080900020004010800050009040301000702000000008006"
#vals = "000 158 000 002 060 800 030 000 040027 030 510000 000 000 046 080 790 050 000 080004 070 100000 325 000"
vals = input("Sudoku string: ")
board_list = string_to_board_list(vals)
display_board(board_list)
print("Original board")
if solve_sudoku(board_list,0):
	print("Solved...")
else:
	print("Too hard")