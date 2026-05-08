from time import sleep
from enum import IntEnum
from typing import Iterator

import openpyxl
from screen_objects import reset_screen

from .objects import objects, ScreenObjectNames
from .status import Status, check_status
from .paths import FARMS_SHEET_PATH


class MineType(IntEnum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    IRON = 3


class Castle:
    alliances_elite_mines: dict[str, int] = {}

    def __init__(self, name: str, lv: int, google: int, account: int, alliance: str):
        self.name: ScreenObjectNames = name # type: ignore
        self.google = google
        self.account = account
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type: MineType = MineType.IRON

    def log_into_account(self) -> None:
        print(f"checking is current castle: {self.name}")
        if not objects[self.name].compare():
            print(f"logging into {self.name}, google: {self.google}, account: {self.account}")
            objects[self.name].tap()
            sleep(0.5)
            objects["account"].tap()
            while True:
                objects['close'].spam_tap(5, 0.1)
                sleep(1)
                objects["switch"].tap()
                sleep(1)
                objects["login"].tap()
                sleep(2)
                if not objects["logo"].compare():
                    continue
                objects["google"].tap(offset_steps=self.google)
                sleep(3)
                if not objects["acc_list"].compare():
                    continue
                objects["castle"].tap(offset_steps=self.account)
                sleep(1)
                objects["confirm"].tap()
                break
            print("logged in.")
            while not any((objects["map"].compare(), objects[self.name].compare(), objects['xs'].tap_if_found())):
                reset_screen()
                sleep(1)
                print("loading...")
            print("loaded.")
        else:
            print(f"already logged into {self.name}")

    def close_ad(self) -> None:
        objects['close'].spam_tap(10, 0.2)
        sleep(1)
        while not objects["map"].compare():
            if not objects["xs"].tap_if_found():
                objects['close'].tap()
            sleep(1)
        print("ad closed.")

    def claim(self) -> None:
        while objects['claim'].tap_if_found():
            print("claimed something")
        sleep(0.5)

    @staticmethod
    def lord_skills() -> None:
        print("lord skills...")
        objects["lord"].tap()
        sleep(0.5)
        objects["harvest"].tap()
        sleep(0.5)
        objects["use"].tap()
        print("harvested. recalling...")
        objects["recall_all"].tap()
        sleep(0.5)
        objects["use"].tap()
        sleep(1)
        objects["close"].tap()
        sleep(0.2)
        objects['close'].tap()
        print("lord skills done.")
    
    @staticmethod
    def heal() -> None:
        if objects["heal"].compare():
            print("healing...")
            objects["heal"].tap()
            sleep(1)
            objects["go"].tap()
            sleep(0.5)
            if objects['confirm_rss'].compare():
                objects['confirm_rss'].tap()
        else:
            print("no need to heal.")
    
    @staticmethod
    def sanctuary() -> None:
        if objects['sanctuary'].compare():
            print("sanctuary...")
            objects['sanctuary'].tap()
            sleep(1)
            objects['go'].tap()
            sleep(0.5)
            objects['back'].tap()
        else:
            print("no need to go to sanctuary.")

    def go_outside(self) -> None:
        print("going outside...")
        objects["map"].tap()
        sleep(2)
        print("outside.")

    def get_std_mine(self) -> None:
        """Go to standard mine from the map."""

        objects["search"].tap()
        while True:
            print(f"searching mine. type: {self.mine_type}, lv: {self.mine_lv}")
            sleep(0.5)
            objects["mine_type"].tap(offset_steps=self.mine_type)
            objects["minus"].spam_tap(5, 0)
            objects["plus"].spam_tap(self.mine_lv - 1, 0)
            objects["go"].spam_tap(4, 0.1)
            sleep(1.5)

            match check_status():
                case Status.FOUND:
                    break
                case Status.NOT_FOUND:
                    if self.mine_type > 0:
                        self.mine_type = MineType(self.mine_type - 1)
                    else:
                        self.mine_lv -= 1
                        self.mine_type = MineType.IRON
                case Status.NOT_MAP:
                    raise(RuntimeError("Not on the map. Panic."))
                case Status.ERROR:
                    print("some chemistry error")
                
        sleep(0.5)
        objects["mine"].tap()
        sleep(0.5)
        objects["gather"].tap()
        sleep(0.5)
        objects["go"].tap()
        print("mine taken.")
        sleep(0.5)
        objects["to_castle"].tap()

    def get_elite_mine(self) -> bool:
        print("Elite")
        while True:
            objects["book"].tap()
            sleep(0.5)
            objects["alliance_elite_mines"].tap()
            sleep(1)
            if objects["blue"].compare(offset_steps=self.alliances_elite_mines.setdefault(self.alliance, 0)):  # color of blue
                objects["blue"].tap(offset_steps=self.alliances_elite_mines[self.alliance])
                sleep(2)
                objects["gather_elite_mine"].tap()
                sleep(0.5)
                objects["go"].tap()  # regularly I should be there
                sleep(0.5)
                objects["to_castle"].tap()
                self.alliances_elite_mines[self.alliance] += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                objects["favorites_back"].tap()
                return False  # if there is no elites


def iter_castles() -> Iterator[Castle]:
    sheet = openpyxl.load_workbook(FARMS_SHEET_PATH).active
    if sheet is None:
        raise ValueError("cannot load sheet")
    
    inp = input("enter from which castle do we start: ") # first row is header

    if not inp:
        for cell in sheet['A'][1:]:
            if objects[cell.value].compare():
                start_row = cell.row
                break
        else:
            raise RuntimeError("cannot find any castle on the screen")
    else:
        start_row = int(inp) + 1 # because of header
    
    for row in sheet.iter_rows(min_row=start_row, values_only=True):
        yield Castle(*row) # type: ignore


""""TODO:
Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)
"""