from subprocess import run

import cv2
from PIL import Image

def make_screen():
    with open(f"screen.png", "wb") as f:
        run(["adb", "exec-out", "screencap", "-p"], stdout = f)
    return Image.open("screen.png")

def make_screen_cv2():
    with open(f"screen.png", "wb") as f:
        run(["adb", "exec-out", "screencap", "-p"], stdout = f)
    return cv2.imread("screen.png")

def get_pixel(screen, cords):
    return screen.getpixel(cords)

def check_color(point_checking: (int, int)):
    return make_screen().getpixel((point_checking[0], point_checking[1]))

def similar_color(color: (int, int, int, int), another_color: (int, int, int, int), tolerance: int) -> bool:
    return all(abs(a - t < tolerance) for a, t in zip(another_color, color))