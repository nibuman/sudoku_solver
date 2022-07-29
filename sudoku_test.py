import unittest
import sudoku
import csv
import time
import json
import datetime


class SudokuSolverTest(unittest.TestCase):

    def setUp(self) -> None:
        with open('./sudoku_data.json', 'r') as f:
            self.config_data = json.load(f)
        return super().setUp()

    def test_clean_string(self) -> None:
        test_input = "12 ;'3df4kkjk5l;n67 8;kf\n9a0"
        test_result = sudoku.clean_string(test_input)
        self.assertEqual(list("1234567890"), test_result)

    def test_sudoku_01(self) -> None:
        self.run_sudoku_solver(puzzle_num=0)

    def test_sudoku_02(self) -> None:
        self.run_sudoku_solver(puzzle_num=1)

    def test_sudoku_03(self) -> None:
        self.run_sudoku_solver(puzzle_num=2)

    def test_sudoku_04(self) -> None:
        self.run_sudoku_solver(puzzle_num=3)

    def test_sudoku_05(self) -> None:
        self.run_sudoku_solver(puzzle_num=4)

    def test_sudoku_06(self) -> None:
        self.run_sudoku_solver(puzzle_num=5)

    def test_sudoku_07(self) -> None:
        self.run_sudoku_solver(puzzle_num=6)

    def test_check_valid_suduko(self):
        # send deliberately invalid suduko boards and check that
        # method fails
        # board 01 start of line 3 should be *37*26...
        # board 02 middle of line 2 should be 793*58*12
        invalid_boards = self.config_data["invalid_boards"]
        for invalid_board in invalid_boards:
            result = sudoku.check_valid_sudoku(invalid_board)
            self.assertEqual(False, result)

        valid_boards = self.config_data['sudoku_puzzle']
        for valid_board in valid_boards:
            result = sudoku.check_valid_sudoku(valid_board["answer"])
            self.assertEqual(True, result)

    def run_sudoku_solver(self, puzzle_num: int):
        """Runs the 'solve_sudoku' method - in separate method
        to keep it consistent for each test. Outputs details of
        each test to a file.
        """

        for alg in (True, False):
            puzzle = self.config_data["sudoku_puzzle"][puzzle_num]["question"]
            answer = self.config_data["sudoku_puzzle"][puzzle_num]["answer"]

            t1 = time.time()
            test_result = sudoku.solve_sudoku(list(puzzle), 0, alg)
            t2 = time.time()

            self.assertEqual(test_result, list(answer))

            # Write out results to file
            csv_row = [datetime.datetime.now(),    # Current date and time
                       "\"" + puzzle + "\"",       # The full puzzle board
                       f'{t2-t1:8.5f}',            # Time to solve
                       sudoku.difficulty_score,    # Difficulty score
                       alg,                        # Algorithm(s) used
                       "v" + sudoku.__version__]   # Version

            with open('sudoku_tst_scores.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(csv_row)

            sudoku.difficulty_score = 0


if __name__ == "__main__":
    unittest.main()
