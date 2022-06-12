def display_board(board_list):
	board = "".join(board_list)
	for a in range(0, 81, 27):
		for b in range(0,27,9):
			n  = a + b
			print(board[n:n+3], " ", board[n+3:n+6], " ", board[n+6:n+9])
		print(" ")
	
def update_available(i, n, cell_defn):	
	cell_defn[i][0].discard(n)
	cell_defn[i][1].discard(n)
	cell_defn[i][2].discard(n)

def solve_sudoku(board, rec_depth):
	print(rec_depth)	
	r = [{str(n) for n in range(1,10)}] * 9
	r1 = {str(n) for n in range(1,10)}
	r2 = r1.copy()
	r3 = r1.copy()
	r4 = r1.copy()
	r5 = r1.copy()
	r6 = r1.copy()
	r7 = r1.copy()
	r8 = r1.copy()
	r9 = r1.copy()
	c1 = {str(n) for n in range(1,10)}
	c2 = c1.copy()
	c3 = c1.copy()
	c4 = c1.copy()
	c5 = c1.copy()
	c6 = c1.copy()
	c7 = c1.copy()
	c8 = c1.copy()
	c9 = c1.copy()
	s1 = {str(n) for n in range(1,10)}
	s2 = s1.copy()
	s3 = s1.copy()
	s4 = s1.copy()
	s5 = s1.copy()
	s6 = s1.copy()
	s7 = s1.copy()
	s8 = s1.copy()
	s9 = s1.copy()
	defn = [[r1, c1, s1], [r1, c2, s1], [r1, c3, s1], [r1, c4, s2], [r1, c5, s2], [r1, c6, s2], [r1, c7, s3], [r1, c8, s3], [r1, c9, s3], \
				[r2, c1, s1], [r2, c2, s1], [r2, c3, s1], [r2, c4, s2], [r2, c5, s2], [r2, c6, s2], [r2, c7, s3], [r2, c8, s3], [r2, c9, s3],\
				[r3, c1, s1], [r3, c2, s1], [r3, c3, s1], [r3, c4, s2], [r3, c5, s2], [r3, c6, s2], [r3, c7, s3], [r3, c8, s3], [r3, c9, s3], \
				[r4, c1, s4], [r4, c2, s4], [r4, c3, s4], [r4, c4, s5], [r4, c5, s5], [r4, c6, s5], [r4, c7, s6], [r4, c8, s6], [r4, c9, s6], \
				[r5, c1, s4], [r5, c2, s4], [r5, c3, s4], [r5, c4, s5], [r5, c5, s5], [r5, c6, s5], [r5, c7, s6], [r5, c8, s6], [r5, c9, s6], \
				[r6, c1, s4], [r6, c2, s4], [r6, c3, s4], [r6, c4, s5], [r6, c5, s5], [r6, c6, s5], [r6, c7, s6], [r6, c8, s6], [r6, c9, s6], \
				[r7, c1, s7], [r7, c2, s7], [r7, c3, s7], [r7, c4, s8], [r7, c5, s8], [r7, c6, s8], [r7, c7, s9], [r7, c8, s9], [r7, c9, s9], \
				[r8, c1, s7], [r8, c2, s7], [r8, c3, s7], [r8, c4, s8], [r8, c5, s8], [r8, c6, s8], [r8, c7, s9], [r8, c8, s9], [r8, c9, s9], \
				[r9, c1, s7], [r9, c2, s7], [r9, c3, s7], [r9, c4, s8], [r9, c5, s8], [r9, c6, s8], [r9, c7, s9], [r9, c8, s9], [r9, c9, s9]]
	print(defn[20][0])
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
			for i,n in enumerate(board):
				if n == "0":
					available = defn[i][0] & defn[i][1] & defn[i][2]
					if len(available) < current_lowest:
						current_lowest = len(available)
						lowest_pos = i
						lowest_available = available.copy()
			for test_num in lowest_available:
				board[lowest_pos] = test_num
				if solve_sudoku(board.copy(), rec_depth+1):
					return True
			return False
	display_board(board)
	return True
		
#vals = list("003020600900305001001806400008102900700000008006708200002609500800203009005010300")
#vals = list("005306078200407005000009106008002034040030010130700500709800000800604001450203600")
#vals = list("069800500000000103400000020000170000080006000307020004000040200630000000850000000")
#vals = list("006080300049070250000405000600317004007000800100826009000702000075040190003090600")
#vals = list("300200000000107000706030500070009080900020004010800050009040301000702000000008006")
vals = list("000158000002060800030000040027030510000000000046080790050000080004070100000325000")

display_board(vals)
print("Original board")
if solve_sudoku(vals,0):
	print("Solved...")
else:
	print("Too hard")