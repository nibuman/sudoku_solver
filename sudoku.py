import logging

from sudoku_solver import plugins, validator, command_line_parser, config, data

DEFAULT_SETTINGS = config.get_defaults()


def main(test_sudoku=None):
    args = command_line_parser.parse_commandline_args()
    logging.basicConfig(
        filename=config.get_filepath("log"),
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info(f"Started with arguments {args}")
    logging.info(f"Default settings: {DEFAULT_SETTINGS}")

    # display the available plugins
    if args.plugin_list:
        plugins.list_plugins()
        exit()
    # Choose input
    if args.board_preset is not None:  # test needed as int(0) is a valid preset
        sudoku_input = data.get_test_sudokus(args.board_preset)
    elif args.input_board:
        sudoku_input = args.input_board
    elif test_sudoku:  # for debugging via python
        sudoku_input = data.get_test_sudokus(test_sudoku)
    else:
        sudoku_input = ""
    logging.info(f"Using input board: {sudoku_input}")
    # maximum number of solutions
    max_results = args.max_results or DEFAULT_SETTINGS.max_solutions
    logging.info(f"Using max_solutions: {max_results}")
    # import user interface
    interface_name = args.user_interface or DEFAULT_SETTINGS.ui
    ui = plugins.import_plugin("ui", interface_name)
    logging.info(f"Using user-interface: {ui.__name__}")
    # import solver
    solver_name = args.solver or DEFAULT_SETTINGS.solver
    solver = plugins.import_plugin("solver", solver_name)
    logging.info(f"Using solver: {solver.__name__}")
    # run the program
    ui.run(sudoku_input, solver.SudokuSolver(), validator, max_results)


if __name__ == "__main__":
    main(1)
