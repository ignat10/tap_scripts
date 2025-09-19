from my_packages.image_tools.image_actions import search_part, is_fullscreen
from my_packages.data.paths import path



def loading():
    folder_path = path["mian_menus"]
    gap = 12
    return search_part(folder_path, gap)


def main_menu():
    folder_path = path["main_menus"]
    gap = 17
    return is_fullscreen(folder_path, gap)


def mine_found() -> bool:
    city = is_city()
    menu = is_menu()
    print(f"city {city} || map/menu {menu}")
    return menu and not city


def is_city() -> bool:
    gap = 0.9
    folder_path = path["cities"]
    return search_part(folder_path, gap)


def is_menu() -> bool:
    folder_path = path["search_menus"]
    gap = 0.9
    return search_part(folder_path, gap)


def visible_gather():
    folder_path = path["gather"]
    gap = 0.8
    return search_part(folder_path, gap)
