import unittest
from sudoku_solver import SudokuSolver
import csv
import time
import json
import datetime


class SudokuSolverTest(unittest.TestCase):
    def setUp(self) -> None:
        with open("./sudoku_data.json", "r") as f:
            self.config_data = json.load(f)
        return super().setUp()

    def test_valid_string(self) -> None:
        # Check that invalid characters are removed
        test_input = """012 ;'3df4kkjk5l;n67 8;kf\n9a
                        01jk2kj3jk4k5l6;l789
                        0123456789
                        0123456789
                        0123456789
                        0123456789
                        0123456#789
                        012345kkljlj67l8l9
                        0
        """
        test_result = sudoku.valid_string(test_input)
        correct_result = ([str(n) for n in range(10)] * 9)[:81]
        self.assertEqual(correct_result, test_result)
        # Check that standard test boards are retrieved
        test_input = "sud01"
        correct_result = list(self.config_data["sudoku_puzzle"][0]["question"])
        test_result = sudoku.valid_string(test_input)
        self.assertEqual(correct_result, test_result)
        # Check that strings of the wrong length are rejected
        test_input = "342qh234h343243"
        test_result = sudoku.valid_string(test_input)
        self.assertEqual(False, test_result)

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
        """Send deliberately invalid suduko boards and check that
        method fails
        board 01 start of line 3 should be *37*26...
        board 02 middle of line 2 should be 793*58*12
        """
        invalid_boards = self.config_data["invalid_boards"]
        for invalid_board in invalid_boards:
            result = SudokuSolver(list(invalid_board)).check_valid()
            self.assertEqual(False, result)

        valid_boards = self.config_data["sudoku_puzzle"]
        for valid_board in valid_boards:
            result = SudokuSolver(list(valid_board["answer"])).check_valid()
            self.assertEqual(valid_board["answer"], result)

    def run_sudoku_solver(self, puzzle_num: int):
        """Runs the 'solve_sudoku' method - in separate method
        to keep it consistent for each test. Outputs details of
        each test to a file.
        """
        puzzle = self.config_data["sudoku_puzzle"][puzzle_num]["question"]
        answer = self.config_data["sudoku_puzzle"][puzzle_num]["answer"]

        t1 = time.time()
        board = SudokuSolver(list(puzzle))
        test_result = board.solve_sudoku()
        t2 = time.time()

        self.assertEqual(test_result, answer)

        # Write out results to file
        csv_row = [
            datetime.datetime.now(),  # Current date and time
            '"' + puzzle + '"',  # The full puzzle board
            f"{t2-t1:8.5f}",  # Time to solve
            board.difficulty_score,  # Difficulty score
            True,
            "v" + SudokuSolver.__version__,
        ]  # Version

        with open("sudoku_tst_scores.csv", "a", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)


if __name__ == "__main__":
    unittest.main()
