import os

os.environ["KIVY_NO_ARGS"] = "1"
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import json
from enum import Enum

sudoku_input = ["0"] * 81
current_pos = None
sudoku_buttons = [None] * 81
solver = None
validator = None
max_solutions = 1


class colour(Enum):
    INPUT_DIGIT = (1, 0, 0, 1)
    SOLVED_DIGIT = (0, 0, 0, 1)


class AppLayout(BoxLayout):
    pass


class AppLabel(Label):
    pass


class AppControls(BoxLayout):
    def reset_board(self):
        global sudoku_input
        for btn in sudoku_buttons:
            btn.text = " "

        sudoku_input = ["0"] * 81

    def quit(self):
        exit()

    def solve(self):
        sudoku_input = "".join(
            [btn.text if btn.text != " " else "0" for btn in sudoku_buttons]
        )

        solved_boards = solver.solve_sudoku(
            sudoku_input, validator.validate_solved_board, max_solutions
        )
        for input_num, solve_num, btn in zip(
            sudoku_input, solved_boards[0], sudoku_buttons
        ):
            if int(input_num):
                btn.color = colour.INPUT_DIGIT.value
                btn.text = solve_num
            else:
                btn.color = colour.SOLVED_DIGIT.value
                btn.text = solve_num


class MyLayout(BoxLayout):
    pass


class OuterGrid(GridLayout):
    pass


class InnerGrid(GridLayout):
    pass


class SudokuButton(Button):
    position = NumericProperty(None)

    def print_number(self):
        print(self.position)
        self.open_keyboard()

    def open_keyboard(self):
        global current_pos
        current_pos = self
        keyboard = NumberEntry()
        keyboard.open()


class NumberEntry(Popup):
    def select_number(self, text):
        sudoku_input[current_pos.position] = text

        print("".join([str(n) for n in sudoku_input]))
        if text == "0":
            current_pos.text = " "
        else:
            current_pos.text = text
            current_pos.color = colour.INPUT_DIGIT.value
        self.dismiss()

    def clear(self):
        self.select_number("0")


class SudokuApp(App):
    def build(self):
        global sudoku_buttons
        thisLayout = MyLayout()
        large_grid = OuterGrid()
        for l_grid in range(9):
            small_grid = InnerGrid()
            for s_grid in range(9):
                pos = (
                    (l_grid // 3) * 27
                    + (l_grid % 3) * 3
                    + (s_grid // 3) * 9
                    + s_grid % 3
                )
                btn = SudokuButton(text=" ", position=pos)
                if int(sudoku_input[pos]):
                    btn.color = colour.INPUT_DIGIT.value
                    # btn.color = "red"
                    btn.text = sudoku_input[pos]
                sudoku_buttons[pos] = btn
                small_grid.add_widget(btn)
            large_grid.add_widget(small_grid)
        thisLayout.add_widget(large_grid)
        return thisLayout


def run(input_board: str | None, _solver, _validator, _max_solutions: int = 1):
    global sudoku_input, solver, validator, max_solutions

    solver = _solver
    validator = _validator
    max_solutions = _max_solutions

    cleaned_board = validator.clean_string(input_board)
    if validator.validate_input_board(cleaned_board):
        sudoku_input = list(cleaned_board)

    app = SudokuApp()
    app.run()


if __name__ == "__main__":
    app = SudokuApp()
    app.run()
