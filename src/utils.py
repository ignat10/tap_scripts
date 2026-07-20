from typing import cast

from .objects import ScreenObjectNames, objects, ScreenObject

object_names = objects.keys()


def object_from_input() -> ScreenObject:
    inp = input("Enter object name: ")
    return object_from_str(inp)


def object_from_str(name: str) -> ScreenObject:
    if name not in object_names:
        raise Exception(f"Object {name} not recognised")
    return objects[cast(ScreenObjectNames, name)]
