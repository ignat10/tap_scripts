from enum import Enum

from my_packages.data.paths import path
from my_packages.data.poco_coordinates import COLORS
from my_packages.image_tools.image_actions import search_part, is_fullscreen, check_color


def loading():
    return not main_menu(15)


def main_menu(gap=17) -> bool:
    folder_path = path["main_menus"]
    return is_fullscreen(folder_path, gap)


def is_city() -> bool:
    gap = 0.8
    folder_path = path["cities"]
    return search_part(folder_path, gap)


def is_menu() -> bool:
    folder_path = path["search_menus"]
    gap = 0.9
    return search_part(folder_path, gap, True)


class Mine(Enum):
    NOT_MAP = 0
    NOT_FOUND = 1
    FOUND_VISIBLE = 2
    FOUND_NOT_VISIBLE = 3


def search_state() -> Mine:
    city = is_city()
    menu = is_menu()

    if not menu:
        return Mine.NOT_MAP

    elif city:
        return Mine.NOT_FOUND

    elif is_visible_gather():
        return Mine.FOUND_VISIBLE

    else:
        return Mine.FOUND_NOT_VISIBLE


def is_visible_gather() -> bool:
    folder_path = path["gather"]
    fullscreen = False
    gap = 0.8
    return search_part(folder_path, gap, fullscreen)


def is_blue(coords) -> bool:
    return check_color(coords) == COLORS["blue"]
