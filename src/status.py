from enum import Enum, IntEnum, auto

from screen_objects import reset_screen

from .objects import objects


class MineType(IntEnum):
    FOOD = 1
    WOOD = 2
    STONE = 3
    IRON = 4


class MapStatus(Enum):
    FOUND = auto()
    NOT_FOUND = auto()
    NOT_AT_MAP = auto()


class CastleStatus(Enum):
    CLOSED_AD = auto()
    AD = auto()
    NOT_IN_CASTLE = auto()


class Status(Enum):
    INSIDE = auto()
    OUTSIDE = auto()
    ELSE = auto()


def check_map_or_castle() -> Status:
    reset_screen()
    if objects['book'].exists():
        return Status.OUTSIDE

    if (
            objects['x'].exists()
            or objects['lord'].exists()
            or objects['claim_daily'].exists()
            or objects['map'].exists()
            or objects['blur'].exists()
    ):
        return Status.INSIDE

    return Status.ELSE


def check_castle_status() -> CastleStatus:
    reset_screen()
    if (
            objects['map'].exists()
            and objects['avatar'].exists()
    ):
        return CastleStatus.CLOSED_AD

    if (
            objects["blur"].exists()
            or objects['claim_daily'].exists()
            or objects['x'].exists()
    ):
        return CastleStatus.AD

    return CastleStatus.NOT_IN_CASTLE


def check_map_status() -> MapStatus:
    reset_screen()
    if not objects['book'].exists():
        return MapStatus.NOT_AT_MAP

    if objects['gather'].exists():
        return MapStatus.FOUND

    return MapStatus.NOT_FOUND
