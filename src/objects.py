from typing import Literal

import screen_objects

from .paths import DATA_DIR


GameObjectNames = Literal[
    "load",
    "xs",
    "close",
    "heal",
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
    "back",
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


objects: dict[GameObjectNames, screen_objects.ScreenObject] = screen_objects.get_objects(DATA_DIR)
