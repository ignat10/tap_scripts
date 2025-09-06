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
    is_city = True if cv2.minMaxLoc(cv2.matchTemplate(fullscreen, city19, cv2.TM_CCORR_NORMED))[1] > 0.95 else False
    is_map = True if cv2.minMaxLoc(cv2.matchTemplate(fullscreen, search_menu, cv2.TM_CCORR_NORMED))[1] > 0.95 else False
    print(f"city {is_city} || map {is_map}")
    return is_map and not is_city

def visible_gather():
    fullscreen = image_actions.make_screen_cv2()
    gather = cv2.imread(path("gather"))
    result = cv2.matchTemplate(fullscreen, gather, cv2.TM_CCORR_NORMED)
    print(f"gather {cv2.minMaxLoc(result)[1]}")
    is_gather = True if cv2.minMaxLoc(result)[1] > 0.90 else False
    return is_gather

if __name__ == "__screen_states__":
    # with open(f"screen.png", "wb") as f:
    #     subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout = f)
    #
    # print("sleep")
    # time.sleep(4)
    #
    # with open("temp.png", "wb") as f:
    #     subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)
    #
    # main = cv2.imread("temp.png")
    # main = cv2.imread(path("mine_found"))
    # part = cv2.imread(path("city19"))
    # result = cv2.matchTemplate(main, part, cv2.TM_CCORR_NORMED)
    # _, max_val, _, max_loc = cv2.minMaxLoc(result)
    # print(max_val, max_loc)
    # screen = cv2.imread("screens/screen.png")
    # img = cv2.imread("screens/screen2.png")
    # print(cv2.PSNR(screen, img))
    print(visible_gather())