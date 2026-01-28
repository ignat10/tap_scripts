from typing import Literal
import json

from .game_object import GameObject
from ..paths import GAME_OBJECTS


GameObjectNames = Literal[
    "load",
    "xs",
    "close",
    "lord",
    "recall_all",
    "harvest",
    "use",
    "map",
    "cities",
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
    "avatar",
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


def load_game_objects():
    global objects
    with GAME_OBJECTS.open() as f:
        raw_data: dict[str, dict[str, tuple[int, int] | int | str | float]] = json.load(f)

    return {
        object_name:
        GameObject(**arguments)
        for object_name, arguments in raw_data.items()
    }


objects: dict[GameObjectNames, GameObject] = load_game_objects()
