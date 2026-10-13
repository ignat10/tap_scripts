from __future__ import annotations

from enum import Enum, auto

from src.objects import objects, tasks, resources_need


class MineType(Enum):
    IRON = objects["iron_type"]
    STONE = objects["stone_type"]
    WOOD = objects["wood_type"]
    FOOD = objects["food_type"]

    @classmethod
    def check_need(cls) -> MineType | None:
        for mine in MineType:
            if mine == MineType.IRON: # WARNING: remove when need_iron template captured
                continue
            if resources_need[mine.name.lower()].exists():
                return mine
        return None


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
        or objects['bella'].exists()
        or objects['x_swap'].exists()
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
    RECRUIT = auto()
    GATHER = auto()
    SCOUT = auto()
    CONQUER = auto()
    ELSE = auto()

    @classmethod
    def check(cls) -> Task:
        for name, obj in tasks.items():
            if obj.exists():
                return cls[name.upper()]
        return cls.ELSE
