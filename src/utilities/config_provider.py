import json
import pathlib

from typing import Any


# noinspection PyBroadException
def config_setup(widget_object_name: str) -> dict[str, Any]:
    config = {}
    try:
        config_path = pathlib.Path(__file__).parents[2].joinpath("config", "app_config.json")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as setup_file:
                config = json.load(setup_file).get(widget_object_name, {})
    except Exception:
        return {}
    return config