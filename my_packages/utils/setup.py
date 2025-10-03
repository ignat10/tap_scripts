from my_packages.adb_helpers.game_actions import Farm
from my_packages.data.farms import accounts, leo
from my_packages.utils.inputter import farm_number


def make_castles() -> list[Farm]:
    castles: list = []
    number = 1
    for google, count in enumerate(accounts[farm_number()::]):
        for account in range(count):
            castles.append(Farm(number, leo[0], google, account, leo[1], leo[2]))
            number += 1
    return castles
