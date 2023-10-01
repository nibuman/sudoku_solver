# Sudoku Solver

Solves sudoku puzzles. Uses a plugin system to allow different solving engines and user interfaces to be used. 

## Installation

Tested in Ubuntu 22.04 LTS
To get a working copy with all the code, in a new directory:
```
git clone https://github.com/nibuman/sudoku_solver
cd sudoku_solver
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install .
```
## Usage

For the command line interface, a string representing a Sudoku board is passed to the program and it returns a solved board.

### Sudoku boards

The string must be contain all 81 digits of the board (where a blank space is represented by '0'), but can have any non-digit characters present as delimiters (such as ' ' or '-').

|   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|
|   |   | 3 |   | 2 |   | 6 |   |   |
| 9 |   |   | 3 |   | 5 |   |   | 1 |
|   |   | 1 | 8 |   | 6 | 4 |   |   |
|   |   | 8 | 1 |   | 2 | 9 |   |   |
| 7 |   |   |   |   |   |   |   | 8 |
|   |   | 6 | 7 |   | 8 | 2 |   |   |
|   |   | 2 | 6 |   | 9 | 5 |   |   |
| 8 |   |   | 2 |   | 3 |   |   | 9 |
|   |   | 5 |   | 1 |   | 3 |   |   |

Would be represented by:
`'0030206009003050010018064000081029007000    00008006708200002609500800203009005010300'`
or:
`'003-020-600-900-305-001-001-806-400-008-102-900-700-0 00-008-006-708-200-002-609-500-800-203-009-005-010-300'`

### Command line interface

- `sudokusolve -h`  help 

- `sudokusolve -p`  get a list of available plugins

- `sudokusolve -i "003020600900305001001806400008102900700000008006708200002609500800203009005010300"`  solve the input board and display using the default display

For testing, to save typing in long strings there are a number of built-in boards that can be run:

- `sudokusolve -b 3` solve built-in Sudoku board number 3 using the default display

- `sudokusolve -b 3 -u "rich_animated_CLI"`  solve built-in Sudoku board number 3 and display using the 'rich_animated_CLI' plugin 

- `sudokusolve -s "solver_python_sets"`  use the 'sudoku_python_sets' solver engine (this is the default)

### GUI interface

Plugins ending in 'GUI' will launch a graphical interface

## Plugins

### Solver plugins

Solver plugins go in the `sudokusolve/solver` directory and must be named with the prefix `solver_` and contain a class that implements `ABCSolver` from `sudokusolve.solver.api` . They need to accept a string of 81 characters as an argument to the `solve_sudoku` method and return a list of solutions (even if there's only 1).

### User interface plugins

User interface plugins go in the `sudokusolver/ui` directory and must be named with the prefix `ui_`. They need a function `run` that is passed any board from the commandline arguments.