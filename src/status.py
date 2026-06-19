from enum import Enum, IntEnum, auto


from .objects import objects


class MineType(IntEnum):
    FOOD = 1
    WOOD = 2
    STONE = 3
    IRON = 4


class Status(Enum):
    ERROR = auto()
    NOT_FOUND = auto()
    FOUND = auto()
    INSIDE_CLOSED = auto()
    INSIDE_AD = auto()


def check_status() -> Status:
    if (
        objects['map'].exists()
        and objects['lord'].exists()
        and objects['avatar'].exists()
    ):
        return Status.INSIDE_CLOSED

    if (
        objects["blur_map"].exists()
        or objects['claim_daily'].exists()
        or objects['x'].exists()
    ):
        return Status.INSIDE_AD

    if not objects['book'].exists():
        return Status.ERROR

    if objects['gather'].exists():
        return Status.FOUND

    return Status.NOT_FOUND
