from time import sleep

from .actions import iter_castles


def farming() -> None:
    for castle in iter_castles():
        castle.log_into_account()
        castle.close_ad()
        castle.claim()
        castle.heal()
        castle.lord_skills()
        castle.to_map()

        for i in range(4):
            if i == 2:
                if not castle.get_elite_mine():
                    if not castle.get_std_mine():
                        break
            else:
                if castle.lv >= 19 or i != 3:
                    if not castle.get_std_mine():
                        break
        else:
            continue
        castle.to_castle()
        castle.recruit()


def seconds():
    for castle in iter_castles():
        castle.log_into_account()
        sleep(15)
