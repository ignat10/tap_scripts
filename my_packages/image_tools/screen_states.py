# libraries
import cv2, time, subprocess

# packages
from my_packages.image_tools import image_actions

screens_path = r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\image_tools\screens\\"
format = r".png"
def path(name: str):
    return screens_path + name + format


def main_menu():
    return

def mine_found():
    fullscreen = image_actions.make_screen_cv2()
    city19 = cv2.imread(path("city19"))
    search_menu = cv2.imread(path("search_mine_menu"))
    city_day = cv2.imread(path("city_day_19"))

    float_city = cv2.minMaxLoc(cv2.matchTemplate(fullscreen, city19, cv2.TM_CCORR_NORMED))[1]
    float_city_day = cv2.minMaxLoc(cv2.matchTemplate(fullscreen, city_day, cv2.TM_CCORR_NORMED))[1]
    float_menu = cv2.minMaxLoc(cv2.matchTemplate(fullscreen, search_menu, cv2.TM_CCORR_NORMED))[1]

    is_city = True if (float_city > 0.95) or (float_city_day > 0.95) else False
    is_map = True if float_menu > 0.95 else False
    print(f"city {float_city}, {is_city} || map {float_menu}, {is_map}")
    return is_map and not is_city

def visible_gather():
    fullscreen = image_actions.make_screen_cv2()
    gather = cv2.imread(path("gather"))
    result = cv2.matchTemplate(fullscreen, gather, cv2.TM_CCORR_NORMED)
    print(f"gather {cv2.minMaxLoc(result)[1]}")
    is_gather = True if cv2.minMaxLoc(result)[1] > 0.90 else False
    return is_gather

if __name__ == "__main__":
    connect_adb()
    with open(f"screen.png", "wb") as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout = f)

    print("sleep")
    time.sleep(4)

    with open("temp.png", "wb") as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)

    main = cv2.imread("screen.png")
    part = cv2.imread(path("event_add3"))
    result = cv2.matchTemplate(main, part, cv2.TM_CCORR_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(max_val, max_loc)