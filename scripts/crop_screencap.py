from os import system


from cv2 import imread, imwrite
from numpy import ndarray


from my_packages.device import actions
from my_packages.game_tools.objects import objects
coords = (505, 1016)


actions.config_serial()
system(f"adb -s {actions.serial} exec-out screencap -p > screen.png")

avatar = objects["cities"]
screen = imread("screen.png")

crop = avatar._crop_screen(screen, coords)

imwrite("cropped_ava.png", crop)
