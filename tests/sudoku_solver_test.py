import csv
import datetime
import json
import time
import unittest

from sudoku_solver import SudokuSolver, BoardError


class SudokuSolverTest(unittest.TestCase):
    def setUp(self) -> None:
        with open("./sudoku_data.json", "r") as f:
            self.config_data = json.load(f)
        self.STANDARD_VALID_INPUT = self.config_data["sudoku_puzzle"][0]["question"]
        self.STANDARD_VALID_SOLVED = self.config_data["sudoku_puzzle"][0]["answer"]
        self.DIGITS_0_TO_9 = {str(n) for n in range(10)}
        self.DIGITS_1_TO_9 = {str(n) for n in range(1, 10)}
        return super().setUp()

    def test_only_valid_digits(self) -> None:
        board = "".join([str(row_num) for row_num in range(9) for _ in range(9)])
        digits = SudokuSolver.DIGITS_0_TO_9
        self.assertTrue(SudokuSolver.only_valid_digits(board, digits))

        invalid_board = f"{board[0:80]}a"
        self.assertFalse(SudokuSolver.only_valid_digits(invalid_board, digits))

    def test_correct_number_of_digits(self) -> None:
        board = "0" * 81
        self.assertTrue(SudokuSolver.correct_number_of_digits(board))

        empty_board = ""
        self.assertFalse(SudokuSolver.correct_number_of_digits(empty_board))

        short_board = "0" * 80
        self.assertFalse(SudokuSolver.correct_number_of_digits(short_board))

    def test_validate_input_board(self) -> None:
        empty_board = ""
        self.assertRaises(BoardError, lambda: SudokuSolver(empty_board))

        valid_board = self.STANDARD_VALID_INPUT
        SudokuSolver(valid_board)

    def test_get_index(self) -> None:
        board = self.STANDARD_VALID_INPUT
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
        board = self.STANDARD_VALID_INPUT
        solver = SudokuSolver(board)

        position = 1
        expected_answer = {"0", "3", "2", "6"}
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

        position = 9
        expected_answer = {"9", "0", "3", "5", "1"}
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

        position = 80
        expected_answer = {"5", "0", "1", "3"}
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

        board = self.STANDARD_VALID_SOLVED
        solver = SudokuSolver(board)

        expected_answer = self.DIGITS_1_TO_9
        position = 80
        answer = solver.get_row(position)
        self.assertEqual(answer, expected_answer)

    def test_get_col(self):
        board = self.STANDARD_VALID_INPUT
        solver = SudokuSolver(board)

        position = 1
        expected_answer = {"0"}
        answer = solver.get_col(position)
        self.assertEqual(answer, expected_answer)

        board = self.STANDARD_VALID_SOLVED
        solver = SudokuSolver(board)

        position = 1
        expected_answer = self.DIGITS_1_TO_9
        answer = solver.get_col(position)
        self.assertEqual(answer, expected_answer)

    def test_get_sqr(self) -> None:
        board = self.STANDARD_VALID_INPUT
        solver = SudokuSolver(board)

        position = 1
        expected_answer = {"3", "0", "9", "1"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 3
        expected_answer = {"0", "2", "3", "5", "8", "6"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 13
        expected_answer = {"0", "2", "3", "5", "8", "6"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 23
        expected_answer = {"0", "2", "3", "5", "8", "6"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 28
        expected_answer = {"0", "8", "7", "6"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        position = 80
        expected_answer = {"5", "0", "9", "3"}
        answer = solver.get_sqr(position)
        self.assertEqual(answer, expected_answer)

        board = self.STANDARD_VALID_SOLVED
        solver = SudokuSolver(board)

        position = 40
        expected_answer = self.DIGITS_1_TO_9
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

    def test_validate_complete_board(self):
        """Send deliberately invalid suduko boards and check that
        method fails
        board 01 start of line 3 should be *37*26...
        board 02 middle of line 2 should be 793*58*12
        """
        # invalid_boards = self.config_data["invalid_boards"]
        # for invalid_board in invalid_boards:
        #     result = SudokuSolver(list(invalid_board)).validate_complete_board()
        #     self.assertEqual(False, result)

        valid_boards = self.config_data["sudoku_puzzle"]
        for valid_board in valid_boards:
            result = SudokuSolver(list(valid_board["answer"])).validate_complete_board()
            self.assertEqual(True, result)

    def test_multiple_solutions(self):
        multiple_boards = self.config_data["multiple_solutions"]
        puzzle = multiple_boards[0]["question"]
        answers = multiple_boards[0]["answers"]

        solver = SudokuSolver(puzzle)
        results = solver.solve_sudoku(16)
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
        solver = SudokuSolver(puzzle)
        results = solver.solve_sudoku(2)
        t2 = time.time()

        self.assertEqual(len(results), 1)
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
