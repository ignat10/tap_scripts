from time import sleep

from my_packages.adb_helpers.adb_config import connect_adb
from my_packages.utils.setup import make_castles



def farming():
    connect_adb()
    castles = make_castles()
    for number, castle in enumerate(castles):
        castle.inside()
        castle.outside()
        castle.second_farm(castles[number + 1])


def seconds():
    connect_adb()
    castles = make_castles()
    for number, castle in enumerate(castles):
        castle.second_farm(castles[number + 1])
        sleep(15)
