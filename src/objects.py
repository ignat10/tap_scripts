from typing import Literal, cast
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from screen_objects import ScreenObject, device_config, get_objects

from . import paths


ScreenObjectNames = Literal[
    "load",
    "xs",
    "close",
    "claim",
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
    "mine_type",
    "plus",
    "minus",
    "mine",
    "gather",
    "go",
    "to_castle",
    "book",
    "favorites_back",
    "alliance_elite_mines",
    "blue",
    "gather_elite_mine",
    "account",
    "switch",
    "login",
    "logo",
    "google",
    "acc_list",
    "castle",
    "confirm",

    "leo",
    "haac",
    "hac",
    "VIC.hac",
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
    