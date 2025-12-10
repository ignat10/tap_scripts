from time import sleep

from ..data.farms import farms



def farming() -> None:
    for castle in farms:
        castle.switch_farm()
        castle.to_map()
        castle.mining()


def seconds():
    for castle in farms:
        castle.switch_farm()
        sleep(15)
