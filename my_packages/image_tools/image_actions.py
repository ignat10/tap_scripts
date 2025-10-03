import cv2
import os
from PIL import Image

from my_packages.core.adb_console import make_screen
from my_packages.data.paths import screen_state_path


def _open_screen_pillow():
    make_screen()
    return Image.open(screen_state_path)


def _open_screen_cv2():
    make_screen()
    return cv2.imread(screen_state_path)


def check_color(point_checking: tuple[int, int]):
    return list[int](_open_screen_pillow().getpixel((point_checking[0], point_checking[1])))


def search_part(folder_path, gap: float, fullscreen=None):
    if fullscreen is None:
        fullscreen = _open_screen_cv2()
    else:
        fullscreen = cv2.imread(screen_state_path)

    for name in os.listdir(folder_path):
        origin = cv2.imread(folder_path / name)
        matched = cv2.matchTemplate(fullscreen, origin, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
        print(f"matched {name}: {max_val}/1.0")
        if max_val > gap:
            return max_loc
    return None


def is_fullscreen(folder_path, gap: int) -> bool:
    fullscreen = _open_screen_cv2()
    for name in os.listdir(folder_path):
        origin = cv2.imread(folder_path / name)
        matched = cv2.PSNR(fullscreen, origin)
        print(f"similarity :{matched}/50")
        if matched > gap:
            return True

    return False
