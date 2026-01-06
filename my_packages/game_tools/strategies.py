from time import sleep


from .farms import farm_generator



farms = farm_generator()


def farming() -> None:
    for castle in farms:
        castle.switch_farm()
        castle.to_map()
        castle.mining()


def seconds():
    for castle in farms:
        castle.switch_farm()
        sleep(15)
