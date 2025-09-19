from os import system


from my_packages.adb_tools.adb_config import get_device_name
from my_packages.data.paths import screen_state_path


device = get_device_name()


def click(cords: (int, int)):
    system(f"adb -s {device} shell input tap {cords[0]} {cords[1]}")


def make_screen():
    system(f"adb -s {device} exec-out screencap -p > {screen_state_path}")