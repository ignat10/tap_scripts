from time import sleep


from .actions import Farm
from ..utils.farms import generator



farms = generator(Farm)


def farming() -> None:
    for castle in farms:
        castle.switch_farm()
        castle.to_map()
        castle.mining()


def seconds():
    for castle in farms:
        castle.switch_farm()
        sleep(15)
