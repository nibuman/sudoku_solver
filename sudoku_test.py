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
        test_input, _ = (
            "003020600900305001001806400"
            "008102900700000008006708200"
            "002609500800203009005010300",
            "483921657967345821251876493"
            "548132976729564138136798245"
            "372689514814253769695417382")
        self.run_sudoku_solver(test_input)

    def test_sudoku_02(self):
        test_input, _ = (
            "005306078200407005000009106"
            "008002034040030010130700500"
            "709800000800604001450203600",
            "915326478286417395374589126"
            "598162734647935812132748569"
            "769851243823674951451293687")
        self.run_sudoku_solver(test_input)

    def test_sudoku_03(self):
        test_input, _ = (
            "069800500000000103400000020"
            "000170000080006000307020004"
            "000040200630000000850000000",
            "169832547528764193473951628"
            "946173852285496371317528964"
            "791345286634289715852617439")
        self.run_sudoku_solver(test_input)

    def test_sudoku_04(self):
        test_input, _ = (
            "006080300049070250000405000"
            "600317004007000800100826009"
            "000702000075040190003090600",
            "516289347849173256732465918"
            "698317524327954861154826739"
            "961732485275648193483591672")
        self.run_sudoku_solver(test_input)

    def test_sudoku_05(self):
        test_input, _ = (
            "800000000003600000070090200"
            "050007000000045700000100030"
            "001000068008500010090000400",
            "812753649943682175675491283"
            "154237896369845721287169534"
            "521974368438526917796318452")
        self.run_sudoku_solver(test_input)

    def test_sudoku_06(self):
        test_input, _ = (
            "005300000800000020070010500"
            "400005300010070006003200080"
            "060500009004000030000009700",
            "145327698839654127672918543"
            "496185372218473956753296481"
            "367542819984761235521839764")
        self.run_sudoku_solver(test_input)

    def test_sudoku_07(self):
        test_input, _ = (
            "000007000100000000000430200"
            "000000006000509000000000418"
            "000081000002000050040000300",
            "238157649174962835569438271"
            "713824596486519723925673418"
            "357281964892346157641795382")
        self.run_sudoku_solver(test_input)

    def test_sudoku_08(self):
        test_input, _ = (
            "000000000000003085001020000"
            "000507000004000100090000000"
            "500000073002010000000040009",
            "987654321246173985351928746"
            "128537694634892157795461832"
            "519286473472319568863745219")
        self.run_sudoku_solver(test_input)

    def test_check_valid_suduko(self):
        # send deliberately invalid suduko boards and check that
        # method fails
        # board 01 start of line 3 should be *37*26...
        # board 02 middle of line 2 should be 793*58*12
        invalid_boards = ("483921657967345821251876493"
                          "548132976729564138136798245"
                          "732689514814253769695417382",
                          "915326478286417395374589126"
                          "598162734647938512132748569"
                          "769851243823674951451293687")
        for invalid_board in invalid_boards:
            result = self.check_valid_sudoku(invalid_board, False)
            self.assertEqual("Fail", result)

    def run_sudoku_solver(self, test_input):
        """Runs the 'solve_sudoku' method - in separate method
        to keep it consistent for each test. Outputs details of
        each test to a file.
        """

        for alg in (True, False):
            cleaned_input = list(test_input)
            t1 = time.time()
            test_result = sudoku.solve_sudoku(cleaned_input, 0, alg)
            t2 = time.time()
            self.check_valid_sudoku(test_result)
            csv_row = ["\"" + test_input + "\""]
            csv_row.append(f'{t2-t1:8.5f}')
            csv_row.append(sudoku.difficulty_score)
            csv_row.append(alg)
            csv_row.append("v" + sudoku.__version__)
            sudoku.difficulty_score = 0
            with open('sudoku_tst_scores.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(csv_row)

    def check_valid_sudoku(self, board: list, run_assert_tests: bool = True):
        """ Checks whether sudoku board is valid by definition
        i.e. is there just one of each digit in each row, column
        and square
        """

        valid_set = {str(n) for n in range(1, 10)}

        # check rows are valid
        for i in range(0, 81, 9):
            row = set(board[i:i+9])
            if run_assert_tests:
                self.assertEqual(valid_set, row)
            elif valid_set != row:
                return "Fail"
        # check columns are valid
        for i in range(9):
            col = set(board[i::9])
            if run_assert_tests:
                self.assertEqual(valid_set, col)
            elif valid_set != col:
                return "Fail"
        # check squares are valid
        for i in range(0, 81, 27):
            for j in range(0, 9, 3):
                sq = []
                for k in range(0, 27, 9):
                    sq.extend(board[i+j+k:i+j+k+3])
                sq = set(sq)
                if run_assert_tests:
                    self.assertEqual(valid_set, sq)
                elif valid_set != sq:
                    return "Fail"
        return "Pass"


if __name__ == "__main__":
    unittest.main()
