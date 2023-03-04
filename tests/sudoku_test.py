import json
import unittest

import sudoku


class Sudoku(unittest.TestCase):
    def setUp(self) -> None:
        with open("./sudoku_data.json", "r") as f:
            self.config_data = json.load(f)
        return super().setUp()

    def test_valid_string(self):
        input_string = "915326478286417395374589126598162734647935812132748569769851243823674951451293687"
        answer = sudoku.valid_string(input_string)
        expected_answer = list(input_string)
        self.assertEqual(answer, expected_answer)

        input_string = "915-326-478tyty2864173..95374589126598162734647935812132748569769851243823674951451293687"
        answer = sudoku.valid_string(input_string)
        self.assertEqual(answer, expected_answer)

        input_string = "afas3232"
        self.assertRaises(ValueError, sudoku.valid_string, input_string)
