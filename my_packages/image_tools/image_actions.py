import cv2, os
from PIL import Image

from my_packages.adb_tools.adb_config import get_device_name
from my_packages.data.paths import screen_state_path
from my_packages.core.adb_tools import make_screen


device = get_device_name()



def open_screen_pillow():
    make_screen()
    return Image.open(screen_state_path)


def open_screen_cv2():
    make_screen()
    return cv2.imread(screen_state_path)



def check_color(point_checking: (int, int)):
    return list[int](open_screen_pillow().getpixel((point_checking[0], point_checking[1])))


def similar_color(color: (int, int, int, int), another_color: (int, int, int, int), tolerance: int) -> bool:
    return all(abs(a - t < tolerance) for a, t in zip(another_color, color))



def search_part(folder_path, gap: float):
    fullscreen = open_screen_cv2()

    for name in os.listdir(folder_path):
        origin = cv2.imread(folder_path / name)
        matched = cv2.matchTemplate(fullscreen, origin, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
        if max_val > gap:
            return max_loc

    return None


def is_fullscreen(folder_path, gap: int) -> bool:
    fullscreen = open_screen_cv2()

    for name in os.listdir(folder_path):
        origin = cv2.imread(folder_path / name)
        matched = cv2.PSNR(fullscreen, origin)
        if matched > gap:
            return True

    return False
