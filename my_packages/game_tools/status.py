from enum import Enum, auto


from . import objects

class Status(Enum):
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def check_status() -> Status:
    if not objects.BOOK.compare_part():
        return Status.NOT_MAP

    if objects.CITIES.find_and_click(do_screen=False):#replace with compare_part
        return Status.NOT_FOUND

    if objects.GATHER.find_and_click(do_screen=False):#replace with compare_part
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE
