"""Loads the settings from the config file.

Expects the config file to be stored in ./data/config.toml and returns the configuration
data as NamedTuples or a dict of NamedTuples. Returning NamedTuple so that the available
options are visible and can be accessed using dot notation.

Typical usage example:

  log_file_path = config.get_filepaths().log_file
  
  default_solver = config.get_defaults().solver
"""
import tomli
import os
from typing import Dict, NamedTuple

PATH_TO_CONFIG_FILE = "data/config.toml"


class DefaultSettings(NamedTuple):
    ui: str
    solver: str
    max_solutions: int


class PluginSettings(NamedTuple):
    description: str
    suffix: str
    entry_point: str


class PathSettings(NamedTuple):
    parent_directory: str
    log_file: str
    data_file: str


defaults = DefaultSettings(None, None, None)
plugins = PluginSettings(None, None, None)
filepaths = PathSettings(None, None, None)
_config_data = None


def initialise(main_file: str):
    global defaults, plugins, filepaths, _config_data
    parent_directory = _get_parent_directory(main_file)
    _config_data = _read_config(parent_directory)
    filepaths = _get_filepaths(parent_directory)
    defaults = _get_defaults()
    plugins = _get_plugins()


def _get_parent_directory(main_file: str):
    absolute_path = os.path.abspath(main_file)
    directory_name = os.path.dirname(absolute_path)
    parent_directory, _ = os.path.split(directory_name)
    return parent_directory


def _get_defaults() -> DefaultSettings:
    return DefaultSettings(
        ui=_config_data["defaults"]["ui"],
        solver=_config_data["defaults"]["solver"],
        max_solutions=_config_data["defaults"]["max_solutions"],
    )


def _get_plugins() -> Dict[str, PluginSettings]:
    plugins = {}
    for plugin in _config_data["plugins"]:
        plugins[plugin] = PluginSettings(
            description=_config_data["plugins"][plugin]["description"],
            suffix=_config_data["plugins"][plugin]["suffix"],
            entry_point=_config_data["plugins"][plugin]["entry_point"],
        )
    return plugins


def _get_filepaths(parent_directory: str):
    data = _read_config(parent_directory)
    return PathSettings(
        parent_directory=parent_directory,
        log_file=f"{parent_directory}/{_config_data['filepaths']['log']}",
        data_file=f"{parent_directory}/{_config_data['filepaths']['data']}",
    )


def _read_config(parent_directory: str) -> Dict:
    with open(f"{parent_directory}/{PATH_TO_CONFIG_FILE}", "rb") as f:
        data = tomli.load(f)
    return data
