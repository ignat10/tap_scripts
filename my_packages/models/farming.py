from my_packages.adb_helpers.adb_config import connect_adb
from my_packages.utils.setup import make_castles


def farming():
    connect_adb()
    castles = make_castles()
    for castle in castles:
        castle.farm_castle()
