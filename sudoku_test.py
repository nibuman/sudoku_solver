import unittest
import sudoku
import csv
import time


class SudokuSolverTest(unittest.TestCase):

    def test_clean_string(self):
        test_input = "12 ;'3df4kkjk5l;n67 8;kf\n9a0"
        test_result = sudoku.clean_string(test_input)
        self.assertEqual(list("1234567890"), test_result)

    def test_sudoku_01(self):
        test_input, correct_result = (
            "003020600900305001001806400"
            "008102900700000008006708200"
            "002609500800203009005010300",
            "483921657967345821251876493"
            "548132976729564138136798245"
            "372689514814253769695417382")
        self.run_sudoku_solver(test_input, correct_result)

    def test_sudoku_02(self):
        test_input, correct_result = (
            "005306078200407005000009106"
            "008002034040030010130700500"
            "709800000800604001450203600",
            "915326478286417395374589126"
            "598162734647935812132748569"
            "769851243823674951451293687")
        self.run_sudoku_solver(test_input, correct_result)

    def test_sudoku_03(self):
        test_input, correct_result = (
            "069800500000000103400000020"
            "000170000080006000307020004"
            "000040200630000000850000000",
            "169832547528764193473951628"
            "946173852285496371317528964"
            "791345286634289715852617439")
        self.run_sudoku_solver(test_input, correct_result)

    def test_sudoku_04(self):
        test_input, correct_result = (
            "006080300049070250000405000"
            "600317004007000800100826009"
            "000702000075040190003090600",
            "516289347849173256732465918"
            "698317524327954861154826739"
            "961732485275648193483591672")
        self.run_sudoku_solver(test_input, correct_result)

    def test_sudoku_05(self):
        test_input, correct_result = (
            "800000000003600000070090200"
            "050007000000045700000100030"
            "001000068008500010090000400",
            "812753649943682175675491283"
            "154237896369845721287169534"
            "521974368438526917796318452")
        self.run_sudoku_solver(test_input, correct_result)

    def test_sudoku_06(self):
        test_input, correct_result = (
            "005300000800000020070010500"
            "400005300010070006003200080"
            "060500009004000030000009700",
            "145327698839654127672918543"
            "496185372218473956753296481"
            "367542819984761235521839764")
        self.run_sudoku_solver(test_input, correct_result)

    def run_sudoku_solver(self, test_input, correct_result):
        """Runs the 'solve_sudoku' method - in separate method
        to keep it consistent for each test
        """

        for alg in (True, False):
            cleaned_input = list(test_input)
            t1 = time.time()
            test_result = sudoku.solve_sudoku(cleaned_input, 0, alg)
            t2 = time.time()
            self.assertEqual(list(correct_result), test_result)
            csv_row = ["\"" + test_input + "\""]
            csv_row.append(f'{t2-t1:8.5f}')
            csv_row.append(sudoku.difficulty_score)
            csv_row.append(alg)
            csv_row.append("v" + sudoku.__version__)
            sudoku.difficulty_score = 0
            with open('sudoku_tst_scores.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(csv_row)


if __name__ == "__main__":
    unittest.main()
