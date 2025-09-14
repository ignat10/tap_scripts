# libraries
import cv2, os, time

from my_packages.adb_tools.adb_config import connect_adb
# packages
from my_packages.image_tools import image_actions

screens_path = r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\image_tools\screens\\"
format = r".png"


def path(name: str):
    return screens_path + name + format

def where_x(fullscreen, name: str):
    print(f"name = {name}")
    part = cv2.imread(path(name))
    match = cv2.matchTemplate(fullscreen, part, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    print(f"name: {name, min_val, max_val, min_loc, max_loc}")
    return max_loc if max_val > 0.9 else None

def main_menu():
    fullscreen = image_actions.open_screen_cv2()
    for i in range(sum(1 for name in os.listdir(screens_path) if "main_menu" in name)):
        part = cv2.imread(path("main_menu" + str(i)))
        result = cv2.PSNR(fullscreen, part)
        print(f"result: {result}")
        if result > 17:
            return True
    return False

def get_coords_add():
    xs = sum(1 for name in os.listdir(screens_path) if "x" in name)
    print(f"xs = {xs}")
    time.sleep(0.2)
    fullscreen = image_actions.open_screen_cv2()
    time.sleep(0.2)
    for i in range(xs):
        coords = where_x(fullscreen, "x" + str(i))
        if coords:
            print(f"found x{i} at {coords}")
            return coords
    return None

def mine_found():
    fullscreen = image_actions.open_screen_cv2()

    city19 = cv2.imread(path("city0"))
    search_menu = cv2.imread(path("search_mine_menu"))
    city_day = cv2.imread(path("city1"))

    float_city = cv2.minMaxLoc(cv2.matchTemplate(fullscreen, city19, cv2.TM_CCORR_NORMED))[1]
    float_city_day = cv2.minMaxLoc(cv2.matchTemplate(fullscreen, city_day, cv2.TM_CCORR_NORMED))[1]
    float_menu = cv2.minMaxLoc(cv2.matchTemplate(fullscreen, search_menu, cv2.TM_CCORR_NORMED))[1]

    is_city = True if (float_city > 0.90) or (float_city_day > 0.95) else False
    is_map = True if float_menu > 0.95 else False
    print(f"city {float_city}, {is_city} || map {float_menu}, {is_map}")
    return is_map and not is_city

def visible_gather():
    fullscreen = image_actions.open_screen_cv2()
    gather = cv2.imread(path("gather"))
    result = cv2.matchTemplate(fullscreen, gather, cv2.TM_CCORR_NORMED)
    print(f"gather {cv2.minMaxLoc(result)[1]}")
    is_gather = True if cv2.minMaxLoc(result)[1] > 0.90 else False
    return is_gather

if __name__ == "__main__":
    print(cv2.PSNR(image_actions.open_screen_cv2(), cv2.imread(path("main_menu1"))))