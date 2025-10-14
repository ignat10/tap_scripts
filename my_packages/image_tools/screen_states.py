from enum import Enum

from my_packages.image_tools.image_actions import search_part, is_full, check_part_screen


def loading() -> bool:
    gap = 0.6
    return not main_menu(gap)


def main_menu(gap=0.8) -> bool:
    folder = "main_menus"
    return is_full(folder, gap)


def is_city() -> bool:
    gap = 0.7
    folder_name = "cities"
    return bool(search_part(folder_name, gap, True))


def is_menu() -> bool:
    folder_name = "search_menus"
    gap = 0.9
    return bool(search_part(folder_name, gap))


class Mine(Enum):
    NOT_MAP = 0
    NOT_FOUND = 1
    FOUND_VISIBLE = 2
    FOUND_NOT_VISIBLE = 3


def search_state() -> Mine:
    if not is_menu():
        return Mine.NOT_MAP

    elif is_city():
        return Mine.NOT_FOUND

    elif is_visible_gather():
        return Mine.FOUND_VISIBLE

    else:
        return Mine.FOUND_NOT_VISIBLE


def is_visible_gather() -> bool:
    folder_name = "gather"
    gap = 0.8
    return bool(search_part(folder_name, gap, True))


def is_blue(coords: tuple[int, int]) -> bool:
    folder = "blue"
    gap = 0.8
    return check_part_screen(folder, coords, gap)