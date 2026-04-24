from enum import Enum, auto


from src.objects import objects



class Status(Enum):
    ERROR = auto()
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def check_status() -> Status:
    if not objects['book'].compare():
        return Status.NOT_MAP

    if not objects['mine'].compare():
        return Status.NOT_FOUND

    if objects['city'].compare():
        return Status.ERROR
    
    if not objects['gather'].compare():
        return Status.FOUND_NOT_VISIBLE

    else:
        return Status.FOUND_VISIBLE
