from typing import TypeVar


T = TypeVar("T")


def inputter(msg: str, base_val: T) -> T:
    type_ = type(base_val)
    string = input(msg)
    try:
        return type_(string)
    except ValueError:
        return base_val
