import tomli
from typing import Dict, NamedTuple


class Defaults(NamedTuple):
    ui: str
    solver: str
    max_solutions: int


class PluginSettings(NamedTuple):
    description: str
    suffix: str
    entry_point: str


def get_defaults() -> Defaults:
    data = _read_config()
    return Defaults(
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


def get_filepath(file_name: str):
    data = _read_config()
    return data["filepaths"][file_name]


def _read_config() -> Dict:
    with open("./data/config.toml", "rb") as f:
        data = tomli.load(f)
    return data
