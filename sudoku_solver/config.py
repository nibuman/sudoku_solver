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

PATH_TO_CONFIG_FILE = "data/config.toml"
parent_directory = ""


class DefaultSettings(NamedTuple):
    ui: str
    solver: str
    max_solutions: int


class PluginSettings(NamedTuple):
    description: str
    suffix: str
    entry_point: str


class PathSettings(NamedTuple):
    log_file: str
    data_file: str


def get_defaults() -> DefaultSettings:
    data = _read_config()
    return DefaultSettings(
        ui=data["defaults"]["ui"],
        solver=data["defaults"]["solver"],
        max_solutions=data["defaults"]["max_solutions"],
    )


def get_plugins() -> Dict[str, PluginSettings]:
    data = _read_config()
    plugins = {}
    for plugin in data["plugins"]:
        plugins[plugin] = PluginSettings(
            description=data["plugins"][plugin]["description"],
            suffix=data["plugins"][plugin]["suffix"],
            entry_point=data["plugins"][plugin]["entry_point"],
        )
    return plugins


def get_filepaths():
    data = _read_config()
    return PathSettings(
        log_file=data["filepaths"]["log"],
        data_file=data["filepaths"]["data"],
    )


def _read_config() -> Dict:
    with open(f"{parent_directory}/{PATH_TO_CONFIG_FILE}", "rb") as f:
        data = tomli.load(f)
    return data
