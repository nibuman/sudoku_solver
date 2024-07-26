"""Discovers and loads plugins.

Types of plugins are defined in the config file.
This module looks in the plugin directory.
for any files that are prefixed with the plugin type,
and can specific plugins as modules.

Typical usage example:
    solver = import_plugin("solver", "solver_python_sets"
"""

import importlib
import importlib.util
import pkgutil
from types import ModuleType
from typing import Dict

from sudokusolve import config


def list_plugins() -> None:
    """Prints a list of available plugins to the terminal"""
    INSTALLED_PLUGINS = find_available_plugins()
    print("Available plugins:")
    for plugin_type in INSTALLED_PLUGINS:
        print(f"    {plugin_type} ({config.plugins[plugin_type].description}):")
        for plugin in INSTALLED_PLUGINS[plugin_type]:
            print(f"        {plugin}")


def import_plugin(plugin_type: str, plugin_name: str) -> ModuleType:
    """Returns the plugin as a module

    Usage:
        solver = import_plugin("solver", "solver_python_sets")
    """
    prefix = config.plugins[plugin_type].prefix
    return importlib.import_module(f"sudokusolve.{plugin_type}.{prefix}{plugin_name}")


def find_available_plugins() -> Dict[str, list[str]]:
    """Returns a dict of the available plugins of the form:
    {plugin_type: [plugin_name1, plugin_name2, ...]}
    """
    plugins: Dict[str, list[str]] = {}
    PLUGIN_TYPES = tuple(config.plugins.keys())
    for plugin_type in PLUGIN_TYPES:
        plugin_prefix = config.plugins[plugin_type].prefix
        plugin_path = config.filepaths.parent_directory / plugin_type
        for module in pkgutil.iter_modules(
            path=[str(plugin_path)]
        ):  # Note that path param takes paths as strings not Path objects
            if module.name.startswith(plugin_prefix):
                module_name = module.name.removeprefix(plugin_prefix)
                try:
                    plugins[plugin_type].append(module_name)
                except KeyError:
                    plugins[plugin_type] = [module_name]
    return plugins
