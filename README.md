# Sudoku Solver

Solves sudoku puzzles. Uses a plugin system to allow different solving engines and user interfaces to be used. 

install with:
```pip install .```

run using:

`sudokusolve -h`  help 

`sudokusolve -p`  get a list of available plugins 

`sudokusolve -b 3` solve standard Sudoku board number 3 

`sudokusolve -u "rich_animated_CLI"`  display the board using the 'rich_animated_CLI' plugin 

`sudokusolve -s "solver_python_sets"`  use the 'sudoku_python_sets' solver engine 

