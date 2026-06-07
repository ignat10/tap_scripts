from enum import Enum, auto


from .objects import objects
from .utils import object_from_str


class Status(Enum):
    ERROR = auto()
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND = auto()


def check_status(level: int) -> Status:
    if not objects['book'].exists():
        return Status.NOT_MAP

    if object_from_str(f'city_{level}').exists():
        return Status.NOT_FOUND
    
    if objects['gather'].exists():
        return Status.FOUND

    else:
        return Status.ERROR
