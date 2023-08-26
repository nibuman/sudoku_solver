import importlib
import importlib.util
import pkgutil
from typing import Dict

PLUGIN_TYPES = ("solver", "ui")


def get_plugins() -> Dict[str, list[str]]:
    plugins: Dict[str, list[str]] = {}
    for plugin_type in PLUGIN_TYPES:
        plugin_suffix = f"{plugin_type}_"
        plugin_path = f"./sudoku_solver/{plugin_type}/"
        for finder, name, ispkg in pkgutil.iter_modules(path=[plugin_path]):
            if name.startswith(plugin_suffix):
                try:
                    plugins[plugin_type].append(name)
                except KeyError:
                    plugins[plugin_type] = [name]

    return plugins


def import_plugin(plugin_type: str, plugin_name: str) -> None:
    pass


SOLVER_PATH = "./sudoku_solver/solver/"
solver_plugins = [
    name
    for finder, name, ispkg in pkgutil.iter_modules(path=[SOLVER_PATH])
    if name.startswith("solver_")
]

# solve_mod = importlib.import_module(f"solver.{solver_plugins[0]}")
# mysolver = solve_mod.SudokuSolver("034242525111")

# x = importlib.util.find_spec(f"solver.{solver_plugins[0]}")
