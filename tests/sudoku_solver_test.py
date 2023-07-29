import csv
import datetime
import json
import time
import unittest

from sudoku_solver import SudokuSolver


class SudokuSolverTest(unittest.TestCase):
    def setUp(self) -> None:
        with open("./sudoku_data.json", "r") as f:
            self.config_data = json.load(f)
        return super().setUp()

    def test_get_index(self) -> None:
        board = "".join([str(row_num) for row_num in range(9) for _ in range(9)])
        solver = SudokuSolver(board)

        position = 0
        expected_answer = (0, 0)
        answer = solver.get_index(position)
        self.assertEqual(answer, expected_answer)

        position = 1
        expected_answer = (0, 1)
        answer = solver.get_index(position)
        self.assertEqual(answer, expected_answer)

        position = 9
        expected_answer = (1, 0)
        answer = solver.get_index(position)
        self.assertEqual(answer, expected_answer)

        position = 20
        expected_answer = (2, 2)
        answer = solver.get_index(position)
        self.assertEqual(answer, expected_answer)

    def test_get_row(self) -> None:
        board = "".join([str(row_num) for row_num in range(9) for _ in range(9)])
        solver = SudokuSolver(board)

        position = 1
        expected_answer = {"0"}
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

        position = 9
        expected_answer = {"1"}
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

        position = 80
        expected_answer = {"8"}
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

        board = "".join([str(row_num) for _ in range(9) for row_num in range(9)])
        solver = SudokuSolver(board)

        full_set = {str(n) for n in range(9)}
        expected_answer = full_set
        position = 80
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

    def test_get_col(self):
        board = "".join([str(row_num) for row_num in range(9) for _ in range(9)])
        solver = SudokuSolver(board)

        position = 1
        full_set = {str(n) for n in range(9)}
        expected_answer = full_set
        answer = solver.get_col(position)
        self.assertEqual(answer, expected_answer)

        board = "".join([str(row_num) for _ in range(9) for row_num in range(9)])
        solver = SudokuSolver(board)

        position = 1
        expected_answer = {"1"}
        answer = solver.get_col(position)
        self.assertEqual(answer, expected_answer)

    def test_get_sqr(self) -> None:
        board = "".join([str(row_num) for row_num in range(9) for _ in range(9)])
        solver = SudokuSolver(board)

        position = 1
        expected_answer = {"0", "1", "2"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 3
        expected_answer = {"0", "1", "2"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 13
        expected_answer = {"0", "1", "2"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 23
        expected_answer = {"0", "1", "2"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 28
        expected_answer = {"3", "4", "5"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 80
        expected_answer = {"6", "7", "8"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

    def test_sudoku_0(self) -> None:
        self.run_sudoku_solver(puzzle_num=0)

    def test_sudoku_1(self) -> None:
        self.run_sudoku_solver(puzzle_num=1)

    def test_sudoku_2(self) -> None:
        self.run_sudoku_solver(puzzle_num=2)

    def test_sudoku_3(self) -> None:
        self.run_sudoku_solver(puzzle_num=3)

    def test_sudoku_4(self) -> None:
        self.run_sudoku_solver(puzzle_num=4)

    def test_sudoku_5(self) -> None:
        self.run_sudoku_solver(puzzle_num=5)

    def test_sudoku_6(self) -> None:
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
            self.assertEqual(True, result)

    def test_multiple_solutions(self):
        multiple_boards = self.config_data["multiple_solutions"]
        puzzle = multiple_boards[0]["question"]
        answers = multiple_boards[0]["answers"]

        solver = SudokuSolver(puzzle, 16)
        results = solver.solve_sudoku()
        expected_number_of_solutions = multiple_boards[0]["solution_count"]
        self.assertEqual(len(results), expected_number_of_solutions)
        # self.assertEqual(len(answers), len(test_result))
        # self.assertEqual(test_result, answers[1])
        test_result = ["".join(result) for result in results]
        for result in test_result:
            self.assertIn(result, answers)

    def run_sudoku_solver(self, puzzle_num: int):
        """Runs the 'solve_sudoku' method - in separate method
        to keep it consistent for each test. Outputs details of
        each test to a file.
        """
        puzzle = self.config_data["sudoku_puzzle"][puzzle_num]["question"]
        answer = self.config_data["sudoku_puzzle"][puzzle_num]["answer"]

        t1 = time.time()
        solver = SudokuSolver(puzzle, 164)
        results = solver.solve_sudoku()
        t2 = time.time()

        test_result = ["".join(result) for result in results]
        self.assertIn(answer, test_result)

        # Write out results to file
        csv_row = [
            datetime.datetime.now(),  # Current date and time
            '"' + puzzle + '"',  # The full puzzle board
            f"{t2-t1:8.5f}",  # Time to solve
            solver.difficulty_score,  # Difficulty score
            True,
            "v" + SudokuSolver.__version__,
        ]  # Version

        with open("sudoku_tst_scores.csv", "a", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)


if __name__ == "__main__":
    unittest.main()
