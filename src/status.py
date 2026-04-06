from enum import Enum, auto


from src.objects import objects



class Status(Enum):
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def check_status() -> Status:
    if not objects['book'].compare():
        return Status.NOT_MAP

    if objects['city'].compare():
        return Status.NOT_FOUND

    if objects['gather'].compare():
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE
