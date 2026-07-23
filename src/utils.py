from typing import cast

from screen_objects import screenshot

from .objects import ScreenObjectNames, objects, ScreenObject

object_names = objects.keys()


def object_from_input() -> ScreenObject:
    inp = input("Enter object name: ")
    return object_from_str(inp)


def object_from_str(name: str) -> ScreenObject:
    if name not in object_names:
        log_raise(f"Object {name} not recognised.")
    return objects[cast(ScreenObjectNames, name)]


def log_raise(msg: str) -> None:
    screenshot()
    raise RuntimeError(f"{msg} Check screen.png for more details.")
