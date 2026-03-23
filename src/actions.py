from time import sleep
from typing import Iterator

import openpyxl

from .objects import objects
from . import status
from .paths import FARMS_SHEET_PATH
from .inputter import inputter


class Castle:
    alliances_elite_mines: dict[str, int] = {}

    def __init__(self, name: str, lv: int, google: int, account: int, alliance: str):
        self.name = name.replace(".", "")
        self.google = google
        self.account = account
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type = 3

    def _switch_account(self) -> None:
        print(f"running second_farm {self.name}, google: {self.google}, account: {self.account}")
        objects[self.name].tap(delay=0.5)
        objects["account"].tap(delay=0.5)
        objects["switch"].tap(delay=1)
        objects["login"].tap(delay=1)
        objects["google"].tap(delay=2, steps=self.google)
        objects["castle"].tap(delay=3, steps=self.account)
        objects["confirm"].tap(delay=1)  # go inside

    def log_into_account(self) -> None:
        print(f"checking is current castle: {self.name}")
        if not objects[self.name].compare():
            self._switch_account()
        print(f"logged into {self.name}")

    def close_ad(self) -> None:
        objects['close'].tap(repeat=5)
        while not objects[self.name].compare():
            if not objects["xs"].find_and_tap():
                objects['close'].tap()
        print("ad closed.")

    @staticmethod
    def lord_skills() -> None:
        print("lord skills...")
        objects["lord"].tap()
        objects["harvest"].tap(delay=0.5)
        objects["use"].tap(delay=0.5)
        print("harvested. recalling...")
        objects["recall_all"].tap()
        objects["use"].tap(delay=0.5)
        objects["close"].tap(repeat=2)
        print("lord skills done.")
    
    @staticmethod
    def heal() -> None:
        print("healing...")
        if objects["hospital"].find_and_tap():
            objects["go"].tap(delay=1)
            objects["confirm_heal_replace_that"].tap(delay=1)

    def go_outside(self) -> None:
        print("going outside...")
        objects["map"].tap()
        sleep(2)
        print("outside.")

    def get_std_mine(self) -> None:
        """Go to standard mine from the map."""

        def find_another_mine() -> None:
            """Find another mine if not found."""
            print(f"searching mine type: {self.mine_type}, lv: {self.mine_lv}")
            objects["mine_type"].tap(steps=self.mine_type, delay=0.5)
            objects["minus"].tap(repeat=5)
            objects["plus"].tap(repeat=self.mine_lv - 1)
            objects["go"].tap(repeat=3)

        def gather_std_mine() -> None:
            objects["gather"].tap(delay=0.5)
            objects["go"].tap(delay=0.5)
            objects["back"].tap(delay=0.5)

        objects["search"].tap(delay=1, repeat=2)
        while True:
            find_another_mine()
            sleep(2)

            match status.check_status():
                case status.Status.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case status.Status.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    objects["gather"].tap()
                    break
                case status.Status.NOT_FOUND:
                    if self.mine_type > 0:
                        print("second mine type")
                        self.mine_type -= 1
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = 3
                case status.Status.NOT_MAP:
                    print("Not on the map. Panic.")
                    continue
        objects["mine"].tap(delay=0.5)
        gather_std_mine()

    def get_elite_mine(self) -> bool:
        print("Elite")
        while True:
            objects["book"].tap()
            objects["alliance_elite_mines"].tap(delay=0.5)
            sleep(1)
            if objects["blue"].compare(steps=self.alliances_elite_mines.setdefault(self.alliance, 0)):  # color of blue
                objects["blue"].tap(steps=self.alliances_elite_mines[self.alliance])
                objects["gather_elite_mine"].tap(delay=2)
                objects["go"].tap(delay=0.5)  # regularly I should be there
                objects["back"]
                self.alliances_elite_mines[self.alliance] += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                objects["favorites_back"].tap()
                return False  # if there is no elites


def iter_castles() -> Iterator[Castle]:
    sheet = openpyxl.load_workbook(FARMS_SHEET_PATH).active
    start_row = inputter("enter from which castle do we start: ", base_val=1) + 1

    for row in sheet.iter_rows(min_row=start_row, values_only=True):
        yield Castle(*row)


""""TODO:
Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)
"""