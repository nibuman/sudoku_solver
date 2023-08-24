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
from sudoku_solver.solver.sudoku_solver import SudokuSolver

sudoku_board = [0] * 81
current_pos = None
sudoku_buttons = [None] * 81


class AppLayout(BoxLayout):
    pass


class AppLabel(Label):
    pass


class AppControls(BoxLayout):
    def reset_board(self):
        global sudoku_board
        for btn in sudoku_buttons:
            btn.text = " "

        sudoku_board = [0] * 81

    def load_preset(self):
        with open("./sudoku_data.json", "r") as f:
            config_data = json.load(f)
            sudoku_input = config_data["sudoku_puzzle"][0]["question"]
            for num, btn in zip(sudoku_input, sudoku_buttons):
                if int(num):
                    # btn.color = (0, 1, 0, 1)
                    btn.color = "red"
                    btn.text = num
                else:
                    btn.text = " "

    def solve(self):
        sudoku_input = "".join(
            [btn.text if btn.text != " " else "0" for btn in sudoku_buttons]
        )

        solver = SudokuSolver(sudoku_input)
        solved_board = solver.solve_sudoku()
        for input_num, solve_num, btn in zip(
            sudoku_input, solved_board, sudoku_buttons
        ):
            if int(input_num):
                btn.color = "red"
                btn.text = solve_num
            else:
                btn.color = "white"
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
        sudoku_board[current_pos.position] = int(text)

        print("".join([str(n) for n in sudoku_board]))
        if text == "0":
            current_pos.text = " "
        else:
            current_pos.text = text
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
                sudoku_buttons[pos] = btn
                small_grid.add_widget(btn)
            large_grid.add_widget(small_grid)
        thisLayout.add_widget(large_grid)
        return thisLayout


if __name__ == "__main__":
    app = SudokuApp()
    app.run()
