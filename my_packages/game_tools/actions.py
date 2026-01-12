from time import sleep
from typing import Self


import openpyxl

from .objects import objects
from . import status
from ..data.paths import FARMS_SHEET_PATH
from ..utils.inputter import inputter


class Farm:
    alliances_elite_mines: dict[Self, int] = {}

    def __init__(self, name: str, lv: int, google: int, account: int, alliance: str):
        self.name = name
        self.google = google
        self.account = account
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type = 0

    @staticmethod
    def lord_skills():
        objects["account"].tap()
        print("lord skills...")
        objects["lord"].click()
        objects["harvest"].click(delay=0.5)
        objects["use"].click(delay=0.5)
        print("harvested. recalling...")
        objects["recall_all"].click()
        objects["use"].click(delay=0.5)
        objects["close"].click()
        objects["close"].click()
        print("lord skills done.")

    def get_std_mine(self):  # to go to basic mine from the map

        def find_another_mine() -> None:  # to find another mine if not found
            objects["mine_type"].click(repeat=self.mine_type)
            objects["minus"].click(repeat=5)
            objects["plus"].click(repeat=self.mine_lv - 1)
            objects["go_mine"].click(repeat=3)

        def gather_std_mine() -> None:
            objects["gather"].click(delay=0.5)
            objects["gather"].click(delay=0.5)
            objects["back"].click(delay=0.5)

        objects["search"].click(delay=1)
        while True:
            find_another_mine()
            sleep(2)
            match status.check_status():
                case status.Status.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case status.Status.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    objects["gather"].click()
                    break
                case status.Status.NOT_FOUND:
                    if self.mine_type < 4:
                        print("second mine type")
                        self.mine_type += 1
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = 0
                case status.Status.NOT_MAP:
                    print("somehow I'm not at the map.\npanic")
                    continue
        objects["mine"].click(delay=0.5)
        sleep(2)
        gather_std_mine()

    def get_elite_mine(self):
        print("Elite")
        while True:
            objects["book"].click()
            objects["alliance_elite_mines"].click(delay=0.5)
            sleep(1)
            if objects["blue"].compare_part():  # color of blue
                objects["blue"].click(steps=self.alliances_elite_mines[self])
                objects["gather_elite_mine"].click(delay=3)
                objects["go"].click(delay=1)  # regularly I should be there
                self.alliances_elite_mines[self] += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                objects["favorites_back"].click()
                return False  # if there is no elites

    def is_current_castle(self) -> bool:
        print(f"checking is current castle: {self.name}")
        return objects[self.name].compare_part()

    def second_farm(self):
        print(f"running second_farm {self.name}, google: {self.google}, account: {self.account}")
        objects["avatar"].click(delay=0.5)
        objects["account"].click(delay=0.5)
        objects["switch"].click(delay=1)
        objects["login"].click(delay=1)
        objects["google"](times=self.google).click(delay=2)
        objects["castle"](times=self.account).click(delay=3)
        objects["confirm"].click(delay=1)  # go inside
        print(f"logged into {self.name}")

    def load(self):
        sleep(1)
        while objects["load"].compare_part():
            print(f"loading {self.name}...")
        print(f"loaded {self.name}")

    @classmethod
    def to_map(cls):
        print("Going to the map...")
        objects["map"].click(repeat=5)
        sleep(2)
        while not objects["book"].compare_part():
            objects["xs"].find_and_click(base_object=objects['map'])
            sleep(1)
        cls.lord_skills()

    def mining(self):
        print("mining...")
        for mine in range(4):
            if mine == 2:
                if self.get_elite_mine():
                    continue
            self.get_std_mine()

    def switch_farm(self):
        if self.is_current_castle():
            print(f"already {self.name}")
        else:
            self.second_farm()
            self.load()

def farm_generator():
    from .actions import Farm
    sheet = openpyxl.load_workbook(FARMS_SHEET_PATH).active
    for row in sheet.iter_rows(min_row=inputter("enter from which google do we start: ", 1) + 1, values_only=True):
        yield Farm(*row)


""""TODO:
Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)
"""