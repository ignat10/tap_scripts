from time import sleep

from ..utils.loaders import make_castles



def farming():
    castles = make_castles()
    for castle in castles:
        print(f"switching to {castle.name}")
        castle.switch_farm()
        castle.inside()
        castle.outside()


def seconds():
    castles = make_castles()
    for castle in castles:
        castle.switch_farm()
        sleep(15)
