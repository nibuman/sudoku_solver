import argparse


def parse_commandline_args():
    parser = argparse.ArgumentParser(
        prog="sudoku", description="Solve any Sudoku puzzle"
    )
    input_parse_group = parser.add_mutually_exclusive_group(required=False)
    input_parse_group.add_argument(
        "-i",
        "--input-board",
        action="store",
        help="use supplied Sudoku string",
        type=str,
    )
    input_parse_group.add_argument(
        "-b",
        "--board-preset",
        help="use preset Sudoku board 1-6",
        action="store",
        choices=range(0, 7),
        type=int,
    )
    input_parse_group.add_argument(
        "-p",
        "--plugin-list",
        action="store_true",
    )
    input_parse_group.add_argument(
        "-v",
        "--version",
        action="version",
        version="0",
    )
    output_parse_group = parser.add_argument_group("Plugins")
    output_parse_group.add_argument(
        "-u",
        "--user-interface",
        help="user interface plugin to use",
        action="store",
        type=str,
    )
    output_parse_group.add_argument(
        "-s",
        "--solver",
        help="solver algorithm plugin to use",
        action="store",
        type=str,
    )
    parser.add_argument(
        "-m",
        "--max-results",
        help="maximum number of solutions to find",
        action="store",
        type=int,
    )
    return parser.parse_args()
