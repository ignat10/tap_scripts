from time import sleep

from my_packages.adb_tools.adb_device import device
from my_packages.loaders.castle_loader import make_castles



def farming():
    device.connect_adb()
    castles = make_castles()
    for castle in castles:
        print(f"switching to {castle.name}")
        castle.switch_farm()
        castle.inside()
        castle.outside()


def seconds():
    device.connect_adb()
    castles = make_castles()
    for castle in castles:
        castle.switch_farm()
        sleep(15)
