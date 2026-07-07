from time import sleep

from .actions import iter_castles


def farming() -> None:
    for castle in iter_castles():
        castle.log_into_account()
        castle.close_ad()
        castle.heal()
        castle.lord_skills()
        castle.to_map()

        if not all(
            castle.get_std_mine() if i != 2 else castle.get_elite_mine()
            for i in range(4)
            if castle.lv >= 19 or i <= 2
        ):
            castle.to_castle()
            castle.recruit()


def seconds():
    for castle in iter_castles():
        castle.log_into_account()
        sleep(15)
