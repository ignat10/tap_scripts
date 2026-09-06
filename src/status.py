from enum import Enum, auto

from src.objects import objects, tasks


class MineType(Enum):
    IRON = objects["iron_type"]
    STONE = objects["stone_type"]
    WOOD = objects["wood_type"]
    FOOD = objects["food_type"]


class MapStatus(Enum):
    FOUND = auto()
    NOT_FOUND = auto()
    NOT_AT_MAP = auto()


class CastleStatus(Enum):
    CLOSED_AD = auto()
    AD = auto()
    NOT_IN_CASTLE = auto()


def check_castle_status() -> CastleStatus:
    if objects["map"].exists():
        return CastleStatus.CLOSED_AD

    if (
        objects["blur"].exists()
        or objects["claim_daily"].exists()
        or objects["x"].exists()
    ):
        return CastleStatus.AD

    return CastleStatus.NOT_IN_CASTLE


def check_map_status() -> MapStatus:
    if not objects["book"].exists():
        return MapStatus.NOT_AT_MAP

    if objects["gather"].exists():
        return MapStatus.FOUND

    return MapStatus.NOT_FOUND


class Task(Enum):
    UPGRADE = auto()
    POWER = auto()
    ELSE = auto()


def check_task() -> Task:
    for name, obj in tasks.items():
        if obj.exists():
            return Task[name.upper()]
    else:
        return Task.ELSE
