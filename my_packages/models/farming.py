from time import sleep

from my_packages.adb_helpers.adb_config import connect_adb
from my_packages.loaders.castle_loader import make_castles



def farming():
    connect_adb()
    castles = make_castles()
    for castle in castles:
        print(f"switching to {castle.name}")
        castle.switch_farm()
        castle.inside()
        castle.outside()


def seconds():
    connect_adb()
    castles = make_castles()
    for castle in castles:
        castle.switch_farm()
        sleep(15)
