"""Discovers and loads plugins.

Types of plugins are defined in the config file. This module looks in the plugin directory
for any files that are prefixed with the plugin type, and can specific plugins as modules.

Typical usage example:
    solver = import_plugin("solver", "solver_python_sets"
"""

import importlib
import importlib.util
import pkgutil
from typing import Dict
from types import ModuleType
from sudoku_solver import config
import os

# os.chdir("/home/nick/Documents/Programming/Sudoku")


def list_plugins() -> None:
    """Prints a list of available plugins to the terminal"""
    print("Available plugins:")
    installed_plugins = get_plugins()
    for plugin_type in installed_plugins:
        print(f"    {plugin_type} ({config.get_plugins()[plugin_type].description}):")
        for plugin in installed_plugins[plugin_type]:
            print(f"        {plugin}")


def import_plugin(plugin_type: str, plugin_name: str) -> ModuleType:
    """Returns the plugin as a module

    Usage:
        solver = import_plugin("solver", "solver_python_sets")
    """
    return importlib.import_module(
        f"sudoku_solver.{plugin_type}.{config.get_plugins()[plugin_type].suffix}"
        f"{plugin_name}"
    )


def get_plugins() -> Dict[str, list[str]]:
    """Returns a dict of the available plugins of the form {plugin_type: [plugin_name1, plugin_name2, ...]}"""
    plugins: Dict[str, list[str]] = {}
    PLUGIN_TYPES = tuple(config.get_plugins().keys())
    for plugin_type in PLUGIN_TYPES:
        plugin_suffix = config.get_plugins()[plugin_type].suffix
        plugin_path = f"{config.parent_directory}/sudoku_solver/{plugin_type}/"
        for finder, name, ispkg in pkgutil.iter_modules(path=[plugin_path]):
            if name.startswith(plugin_suffix):
                try:
                    plugins[plugin_type].append(_strip_prefix(name, plugin_type))
                except KeyError:
                    plugins[plugin_type] = [_strip_prefix(name, plugin_type)]
    return plugins


def _strip_prefix(plugin: str, plugintype) -> str:
    return plugin.removeprefix(f"{plugintype}_")
