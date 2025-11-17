from time import sleep

from .actions import make_castles

castles = make_castles()


def farming() -> None:
    for castle in castles:
        castle.switch_farm()
        castle.inside()
        castle.outside()


def seconds():
    for castle in castles:
        castle.switch_farm()
        sleep(15)
