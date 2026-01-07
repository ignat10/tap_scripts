from enum import Enum, auto


from ..data import objects

class Status(Enum):
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def check_status() -> Status:
    if not objects.BOOK.compare_part():
        return Status.NOT_MAP

    if objects.CITIES.find_part(do_screen=False):
        return Status.NOT_FOUND

    if objects.GATHER.find_part(do_screen=False):
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE
