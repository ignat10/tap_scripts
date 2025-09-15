from subprocess import run

import cv2
from PIL import Image

from my_packages.adb_tools.adb_config import get_device_name
from my_packages.data.paths import temp_screen_path

device = get_device_name()

def make_screen():
    with open(temp_screen_path, "wb") as f:
        run(["adb", "-s", device, "exec-out", "screencap", "-p"], stdout = f)

def open_screen_PIL():
    make_screen()
    return Image.open(temp_screen_path)

def open_screen_cv2():
    make_screen()
    return cv2.imread(temp_screen_path)


def check_color(point_checking: (int, int)):
    return list[int](open_screen_PIL().getpixel((point_checking[0], point_checking[1])))

def similar_color(color: (int, int, int, int), another_color: (int, int, int, int), tolerance: int) -> bool:
    return all(abs(a - t < tolerance) for a, t in zip(another_color, color))