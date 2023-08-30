import json
import logging

from sudoku_solver import plugins, validator, command_line_parser, config


# TODO: put into separate module
def get_test_sudokus(puzzle_num: int) -> str:
    """Retrieves the test Sudoku boards from the config file"""
    assert 0 <= puzzle_num < 7, f"Test Sudoku must be 0-6,{puzzle_num} given"
    with open("./data/sudoku_data.json", "r") as f:
        config_data = json.load(f)
    return config_data["sudoku_puzzle"][puzzle_num]["question"]


# TODO: move to plugins module?
def list_plugins() -> None:
    print("Available plugins:")
    installed_plugins = plugins.get_plugins(
        ["solver", "ui"]
    )  # TODO put supported plugins in config
    for plugin_type in installed_plugins:
        print(f"    {plugin_type}:")
        for plugin in installed_plugins[plugin_type]:
            print(f"        {plugin}")


def main(test_sudoku=None):
    args = command_line_parser.parse_commandline_args()
    default_settings = config.get_defaults()
    logging.basicConfig(
        filename="./data/sudoku_solver.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info(f"Started with arguments {args}")
    logging.info(f"Default settings: {default_settings}")

    # display the available plugins
    if args.plugin_list:
        list_plugins()
        exit()
    # Choose input
    if args.board_preset is not None:  # test needed as int(0) is a valid preset
        sudoku_input = get_test_sudokus(args.board_preset)
    elif args.input_board:
        sudoku_input = args.input_board
    elif test_sudoku:  # for debugging via python
        sudoku_input = get_test_sudokus(test_sudoku)
    else:
        sudoku_input = ""
    logging.info(f"Using input board: {sudoku_input}")
    # import user interface
    interface_name = args.user_interface or default_settings.ui
    ui = plugins.import_plugin("ui", interface_name)
    logging.info(f"Using user-interface: {ui.__name__}")
    # import solver
    solver_name = args.solver or default_settings.solver
    solver = plugins.import_plugin("solver", solver_name)
    logging.info(f"Using solver: {solver.__name__}")
    # run the program
    ui.run(sudoku_input, solver.SudokuSolver(), validator, args.max_results)


if __name__ == "__main__":
    main(1)
