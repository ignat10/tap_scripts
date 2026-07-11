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

        for i in range(castle.free_marches() - 1): # - 1 for elite mine
            if castle.is_enough_troops:
                castle.get_std_mine()
            else:
                break
        else:
            if castle.get_elite_mine() is False:
                castle.get_std_mine()

            if castle.free_marches() == 0:
                castle.is_enough_troops = True

        if not castle.is_enough_troops:
            castle.to_castle()
            castle.recruit()


def seconds():
    for castle in iter_castles():
        castle.log_into_account()
        sleep(15)
