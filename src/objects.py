from typing import Literal, cast
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from screen_objects import ScreenObject, device_config, get_objects

from . import paths


ScreenObjectNames = Literal[
    "x1",
    "close",
    "claim",
    "hospital",
    "heal",
    "confirm_rss",
    "sanctuary",
    "back",
    "lord",
    "recall_all",
    "harvest",
    "use",
    "map",
    "city",
    "search",
    "food",
    "wood",
    "stone",
    "iron",
    "plus",
    "minus",
    "food_type",
    "wood_type",
    "stone_type",
    "iron_type",
    "go",
    "gather",
    "set_out",
    "to_castle",
    "book",
    "elite_mines",
    "blue",
    "gather_elite",
    "account",
    "switch",
    "login",
    "logo",
    "mail",
    "acc_list",
    "castle",
    "confirm",

    "leo",
    "haac",
    "hac",
    "VIChac",
    "farm,hacen",
    "kazuru_farm5",
    "kazuru_farm6",
]



objects: dict[ScreenObjectNames, ScreenObject] = cast(
    dict[ScreenObjectNames, ScreenObject],
    get_objects(paths.SAMPLES_DIR)
)


def config():
    load_dotenv()
    adb = getenv("ADB")
    if adb is None:
        raise Exception("ADB not set")
    device_config(adb=Path(adb), ip=None)
    