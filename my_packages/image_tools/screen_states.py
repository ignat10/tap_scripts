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
    part = cv2.imread(path("citi19"))
    result = cv2.matchTemplate(fullscreen, part, cv2.TM_CCORR_NORMED)
    return result[1]

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
print(mine_found())