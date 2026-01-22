from os import system

from cv2 import imread, imwrite

from src.device import actions
from src.game_tools.objects import objects



actions.config_serial()
system(f"adb -s {actions.serial} exec-out screencap -p > screen.png")

key = input("enter what template are we capturing: ")
template = objects[key]


screen = imread("screen.png")

crop = template._crop_screen(screen)

imwrite("cropped_screen.png", crop)
