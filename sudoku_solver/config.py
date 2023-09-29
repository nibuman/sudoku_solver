"""Loads the settings from the config file.

Expects the config file to be stored in ./data/config.toml and returns the configuration
data as NamedTuples or a dict of NamedTuples. Returning NamedTuple so that the available
options are visible and can be accessed using dot notation.

Typical usage example:

  log_file_path = config.get_filepaths().log_file
  
  default_solver = config.get_defaults().solver
"""
import tomli
from typing import Dict, NamedTuple
from pathlib import Path

PATH_TO_CONFIG_FILE = "data/config.toml"


class DefaultSettings(NamedTuple):
    ui: str
    solver: str
    max_solutions: int


class PluginSettings(NamedTuple):
    description: str
    prefix: str
    entry_point: str


class PathSettings(NamedTuple):
    parent_directory: Path
    log_file: Path
    data_file: Path


defaults = DefaultSettings("", "", 1)
plugins = {}
filepaths = PathSettings(Path(), Path(), Path())
_config_data = {}


def initialise():
    global defaults, plugins, filepaths, _config_data
    parent_directory = Path(__file__).parents[1]
    _config_data = _read_config(parent_directory)
    filepaths = _get_filepaths(parent_directory)
    defaults = _get_defaults()
    plugins = _get_plugins()


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
            prefix=_config_data["plugins"][plugin]["prefix"],
            entry_point=_config_data["plugins"][plugin]["entry_point"],
        )
    return plugins


def _get_filepaths(parent_directory: Path):
    return PathSettings(
        parent_directory=parent_directory,
        log_file=parent_directory / _config_data["filepaths"]["log"],
        data_file=parent_directory / _config_data["filepaths"]["data"],
    )


def _read_config(parent_directory: Path) -> Dict:
    with open(parent_directory / PATH_TO_CONFIG_FILE, "rb") as f:
        data = tomli.load(f)
    return data


initialise()
