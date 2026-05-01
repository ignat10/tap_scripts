from enum import Enum, auto


from src.objects import objects



class Status(Enum):
    ERROR = auto()
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND = auto()


def check_status() -> Status:
    if not objects['book'].compare():
        return Status.NOT_MAP

    if objects['city'].compare():
        return Status.NOT_FOUND
    
    if objects['gather'].compare() or objects['mine'].compare():
        return Status.FOUND

    else:
        return Status.ERROR
