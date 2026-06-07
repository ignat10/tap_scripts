from typing import Literal, cast
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from screen_objects import ScreenObject, device_config, get_objects

from . import paths


ScreenObjectNames = Literal[
    "claim_daily",
    "x1",
    "blur_map",
    "claim_healed",
    "hospital",
    "heal",
    "confirm_rss",
    "ask_help",
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

    "leo",
    "haac",
    "hac",
    "VIChac",
    'farm,hacen',
    "kazuru_farm5",
    "kazuru_farm6",

    "avatar",
    "account",
    "switch",
    "login",
    "logo",

    "google_1",
    "google_2",

    "acc_list",

    "leo_account",
    "haac_account",
    "hac_account",

    "confirm",
]



objects: dict[ScreenObjectNames, ScreenObject] = cast(
    dict[ScreenObjectNames, ScreenObject],
    get_objects(paths.SAMPLES_DIR)
)


def config():
    load_dotenv()
    adb = getenv("ADB")
    ip = getenv("IP")
    if adb is None:
        raise Exception("ADB not set. set adb path in .env file.")
    device_config(adb=Path(adb), ip=ip)
    