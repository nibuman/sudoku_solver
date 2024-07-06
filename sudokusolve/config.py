"""Loads the settings from the config file.

Expects the config file to be stored in ./data/config.toml and returns the configuration
data as NamedTuples or a dict of NamedTuples. Returning NamedTuple so that the available
options are visible and can be accessed using dot notation.

Typical usage example:

  log_file_path = config.get_filepaths().log_file

  default_solver = config.get_defaults().solver
"""

from pathlib import Path
from typing import Dict, NamedTuple

import tomllib

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


def _get_defaults(config_data: Dict) -> DefaultSettings:
    return DefaultSettings(**config_data["defaults"])


def _get_plugins(config_data: Dict) -> Dict[str, PluginSettings]:
    plugins = config_data["plugins"]
    return {name: PluginSettings(**plugins[name]) for name in plugins}


def _get_filepaths(config_data: Dict, parent_directory: Path):
    return PathSettings(
        parent_directory=parent_directory,
        log_file=parent_directory / config_data["filepaths"]["log_file"],
        data_file=parent_directory / config_data["filepaths"]["data_file"],
    )


def _read_config(parent_directory: Path) -> Dict:
    with open(parent_directory / PATH_TO_CONFIG_FILE, "rb") as f:
        data = tomllib.load(f)
    return data


_parent_directory = Path(__file__).parent
_config_data = _read_config(_parent_directory)
defaults = _get_defaults(config_data=_config_data)
filepaths = _get_filepaths(config_data=_config_data, parent_directory=_parent_directory)
plugins = _get_plugins(config_data=_config_data)
