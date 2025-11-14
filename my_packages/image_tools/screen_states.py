from enum import Enum

from my_packages.image_tools.image_analyzer import match_screen, find_part, compare_part


class Status(Enum):
    NOT_MAP = 0
    NOT_FOUND = 1
    FOUND_VISIBLE = 2
    FOUND_NOT_VISIBLE = 3


def loading() -> bool:
    gap = 0.6
    folder = "ads"
    return not match_screen(folder, gap)


def main_menu(gap=0.8) -> bool:
    folder = "main_menus"
    return match_screen(folder, gap)


def is_city() -> bool:
    gap = 0.6
    folder_name = "cities"
    result = find_part(folder_name, gap, True)
    return result


def is_menu() -> bool:
    folder_name = "search_menus"
    gap = 0.9
    return find_part(folder_name, gap)

def check_status() -> Status:
    if not is_menu():
        return Status.NOT_MAP

    elif is_city():
        return Status.NOT_FOUND

    elif is_visible_gather():
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE


def is_visible_gather() -> bool:
    folder_name = "gather"
    gap = 0.6
    result = find_part(folder_name, gap, False)
    return bool(result)


def is_blue(coords: tuple[int, int]) -> bool:
    folder_name = "blue"
    gap = 0.8
    return compare_part(folder_name, gap, coords)


def get_coords() -> tuple[int, int] | None:
    folder_name = "xs"
    gap = 0.9
    return find_part(folder_name, gap, False)


def is_avatar(castle_name: str) -> bool:
    gap = 0.8
    ava = find_part(castle_name, gap)
    return bool(ava)
