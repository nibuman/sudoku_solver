import importlib
import importlib.util
import pkgutil
from typing import Dict
from types import ModuleType

PLUGIN_TYPES = ("solver", "ui")


def strip_prefix(plugin: str, plugintype) -> str:
    return plugin.removeprefix(f"{plugintype}_")


def get_plugins(plugin_types: list[str]) -> Dict[str, list[str]]:
    plugins: Dict[str, list[str]] = {}
    for plugin_type in PLUGIN_TYPES:
        plugin_suffix = f"{plugin_type}_"
        plugin_path = f"./sudoku_solver/{plugin_type}/"
        for finder, name, ispkg in pkgutil.iter_modules(path=[plugin_path]):
            if name.startswith(plugin_suffix):
                try:
                    plugins[plugin_type].append(strip_prefix(name, plugin_type))
                except KeyError:
                    plugins[plugin_type] = [strip_prefix(name, plugin_type)]
    return plugins


def import_plugin(plugin_type: str, plugin_name: str) -> ModuleType:
    return importlib.import_module(
        f"sudoku_solver.{plugin_type}.{plugin_type}_{plugin_name}"
    )
