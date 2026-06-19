from typing import Literal, cast
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from screen_objects import ScreenObject, device_config, get_objects

from . import paths


ScreenObjectNames = Literal[
    "claim_daily",
    "blur_map",
    "x",
    "claim_healed",
    "hospital",
    "heal",
    "confirm_rss",
    "ask_help",
    "hospital_building",
    "speed_up",
    "one-tap_speed_up",
    "confirm_speed_up",
    "sanctuary",
    "claim_holy_water",
    "confirm_claim_water",
    "holy_quest",
    "claim_holy_quest",
    "holy_revival",
    "revive",
    "lord",
    "recall_all",
    "harvest",
    "gather_speed_up",
    "use",
    "map",
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
    "city_15",
    "city_19",
    "gather",
    "set_out",
    "book",
    "elite_mines",
    "blue",
    "check",
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

    "google_1",
    "google_2",
    "google_3",
    "google_4",

    "acc_list",

    "leo_account",
    "haac_account",
    "hac_account",
    "farm,hacen_account",
    'VIChac_account',
    'kazuru_farm5_account',
    'kazuru_farm6_account',

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
    