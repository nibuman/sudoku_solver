import importlib
import importlib.util
import pkgutil
from typing import Dict
from types import ModuleType
from sudoku_solver import config


PLUGIN_SETTINGS = config.get_plugins()
PLUGIN_TYPES = tuple(PLUGIN_SETTINGS.keys())
PARENT_DIRECTORY = "sudoku_solver"


def list_plugins() -> None:
    print("Available plugins:")
    installed_plugins = get_plugins()
    for plugin_type in installed_plugins:
        print(f"    {plugin_type} ({PLUGIN_SETTINGS[plugin_type].description}):")
        for plugin in installed_plugins[plugin_type]:
            print(f"        {plugin}")


def import_plugin(plugin_type: str, plugin_name: str) -> ModuleType:
    return importlib.import_module(
        f"{PARENT_DIRECTORY}.{plugin_type}.{PLUGIN_SETTINGS[plugin_type].suffix}"
        f"{plugin_name}"
    )


def get_plugins() -> Dict[str, list[str]]:
    plugins: Dict[str, list[str]] = {}
    for plugin_type in PLUGIN_TYPES:
        plugin_suffix = PLUGIN_SETTINGS[plugin_type].suffix
        plugin_path = f"./{PARENT_DIRECTORY}/{plugin_type}/"
        for finder, name, ispkg in pkgutil.iter_modules(path=[plugin_path]):
            if name.startswith(plugin_suffix):
                try:
                    plugins[plugin_type].append(_strip_prefix(name, plugin_type))
                except KeyError:
                    plugins[plugin_type] = [_strip_prefix(name, plugin_type)]
    return plugins


def _strip_prefix(plugin: str, plugintype) -> str:
    return plugin.removeprefix(f"{plugintype}_")
