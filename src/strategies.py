from time import sleep

from .actions import iter_castles
from .objects import config


config()


def farming() -> None:
    for castle in iter_castles():
        castle.log_into_account()
        castle.close_ad()
        castle.heal()
        castle.lord_skills()
        castle.go_outside()

        castle.get_std_mine()
        castle.get_std_mine()
        if not castle.get_elite_mine():
            castle.get_std_mine()
        if castle.lv >= 19:
            castle.get_std_mine()


def seconds():
    for castle in iter_castles():
        castle.log_into_account()
        sleep(15)
