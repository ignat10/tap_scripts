from typing import Literal

import screen_objects

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
    "google",
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

ip = paths.IP_PATH.read_text()

objects: dict[ScreenObjectNames, screen_objects.ScreenObject] = screen_objects.get_objects(paths.SAMPLES_DIR, paths.OBJECTS_PATH, ip) # type: ignore
