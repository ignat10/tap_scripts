# libraries
from os import system
from subprocess import run

# packages
from my_packages.adb_tools.adb_config import get_device_name
from my_packages.data.paths import temp_screen_path

device = get_device_name()
def click(cords: (int, int)):
    system(f"adb -s {device} shell input tap {cords[0]} {cords[1]}")


def make_screen():
    with open(temp_screen_path, "wb") as f:
        run(["adb", "-s", device, "exec-out", "screencap", "-p"], stdout = f)