import tomli
from typing import Dict, NamedTuple


class Settings(NamedTuple):
    ui: str
    solver: str


def get_defaults() -> Settings:
    data = _read_config()
    return Settings(
        ui=data["defaults"]["ui"],
        solver=data["defaults"]["solver"],
    )


def _read_config() -> Dict:
    with open("./data/config.toml", "rb") as f:
        data = tomli.load(f)
    return data
