from __future__ import annotations

from enum import Enum, auto

from src.objects import objects, resources_need


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

class Task(Enum):
    UPGRADE = objects["start_upgrading"]
    POWER = objects["battle_power"]
    RECRUIT = objects["recruit_"]
    SCOUT = objects["scout"]
    CONQUER = objects["conquer"]
    GATHER = objects["gather_task"]
    RUINS = objects["ruins_wave_3"]

    @classmethod
    def check(cls) -> Task | None:
        for task in cls:
            if task.value.exists():
                return task
        return None
