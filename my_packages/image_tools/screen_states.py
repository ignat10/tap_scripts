# libraries
import cv2, os, time

from my_packages.adb_tools.adb_config import connect_adb
# packages
from my_packages.image_tools import image_actions
from my_packages.data.paths import screens_path, format


def path(folder_path: str, name: str):
    return folder_path + name + format



def loading():
    folder_path = screens_path + r"main_menus\\"
    fullscreen = image_actions.open_screen_cv2()
    for name in os.listdir(folder_path):
        origin = cv2.imread(folder_path + name)
        result = cv2.PSNR(fullscreen, origin)
        print(f"result [{name}]: {result}")
        if result > 12:
            return False
    return True

def main_menu():
    folder_path = screens_path + r"main_menus\\"
    fullscreen = image_actions.open_screen_cv2()

    for name in os.listdir(folder_path):
        part = cv2.imread(folder_path + name)
        result = cv2.PSNR(fullscreen, part)
        print(f"result: {result}")
        if result > 17:
            return True

    return False


def where_x(fullscreen, x_path: str):
    part = cv2.imread(x_path)
    match = cv2.matchTemplate(fullscreen, part, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    print(f"name: {min_val, max_val, min_loc, max_loc}")
    return max_loc if max_val > 0.9 else None


def get_coords_add():
    folder_path = screens_path + r"xs\\"
    fullscreen = image_actions.open_screen_cv2()

    for name in os.listdir(folder_path):
        coords = where_x(fullscreen, folder_path + name)
        if coords:
            print(f"found {name} at {coords}")
            return coords
    return None

def mine_found() -> bool:
    city = is_city()
    menu = is_menu()

    print(f"city {city} || map/menu {menu}")
    return menu and not city

def is_city() -> bool:
    GAP = 0.9
    folder_path = screens_path + r"map\cities\\"

    return is_screen(folder_path, GAP)

def is_menu() -> bool:
    folder_path = screens_path + r"map\search_menus\\"
    GAP = 0.9

    return is_screen(folder_path, GAP)

def is_screen(folder_path, GAP: float) -> bool:
    fullscreen = image_actions.open_screen_cv2()

    for name in os.listdir(folder_path):
        origin = cv2.imread(folder_path + name)
        matched = cv2.matchTemplate(fullscreen, origin, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(matched)
        if max_val > GAP:
            return True

    return False

def visible_gather():
    folder_path = str(screens_path + r"map\\" + r"gather\\")
    GAP = 0.8

    return is_screen(folder_path, GAP)

if __name__ == "__main__":
    print(cv2.PSNR(image_actions.open_screen_cv2(), cv2.imread(path("main_menu1"))))