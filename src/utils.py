from typing import get_args, cast

from .objects import ScreenObjectNames, objects, ScreenObject

object_names = get_args(ScreenObjectNames)

def object_from_input() -> ScreenObject:
    while (inp := input("Enter object name: ")) not in object_names:
        print("Object name not recognised")
    return objects[cast(ScreenObjectNames, inp)]
