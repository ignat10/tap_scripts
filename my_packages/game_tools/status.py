from enum import Enum, auto


from ..image_tools import templates


class Status(Enum):
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def check_status() -> Status:
    if not templates.BOOK.compare_part():
        return Status.NOT_MAP

    if templates.CITIES.find_part(do_screen=False):
        return Status.NOT_FOUND

    if templates.GATHER.find_part(do_screen=False):
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE
