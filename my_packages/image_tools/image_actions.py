from subprocess import run

import cv2
from PIL import Image

from my_packages.adb_tools.adb_config import get_device_name

device = get_device_name()

def make_screen():
    with open(f"screen.png", "wb") as f:
        run(["adb", "-s", device, "exec-out", "screencap", "-p"], stdout = f)

def open_screen_PIL():
    make_screen()
    return Image.open(f"screen.png")

def make_screen_cv2():
    make_screen()
    return cv2.imread("screen.png")

def get_pixel(screen, cords):
    return screen.getpixel(cords)

def check_color(point_checking: (int, int)):
    return make_screen().getpixel((point_checking[0], point_checking[1]))

def similar_color(color: (int, int, int, int), another_color: (int, int, int, int), tolerance: int) -> bool:
    return all(abs(a - t < tolerance) for a, t in zip(another_color, color))