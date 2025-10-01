from my_packages.utils.inputter import farm_number
from my_packages.adb_tools.game_actions import Farm

accounts = [1, 2, 2, 2, 2]
number = 1

leo = ("leo", 19, "MIA")


castles: list = []
for google in range(farm_number(), len(accounts)):
    for account in range(accounts[google]):
        castles.append(Farm(number, leo[0], google, account, leo[1], leo[2]))
        number += 1