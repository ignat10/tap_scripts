from enum import Enum, auto


from src.objects import objects



class Status(Enum):
    ERROR = auto()
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND = auto()


def check_status() -> Status:
    if not objects['book'].exists():
        return Status.NOT_MAP

    if objects['city'].exists():
        return Status.NOT_FOUND
    
    if objects['gather'].exists() or objects['mine'].exists():
        return Status.FOUND

    else:
        return Status.ERROR
