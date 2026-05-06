from time import sleep
from enum import IntEnum
from typing import Iterator

import openpyxl
from screen_objects import reset_screen

from .objects import objects, ScreenObjectNames
from .status import Status, check_status
from .paths import FARMS_SHEET_PATH
from .inputter import inputter


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
        objects['close'].tap(repeat=5)
        while not objects["map"].compare():
            if not objects["xs"].tap_if_found():
                objects['close'].tap()
        print("ad closed.")

    def claim(self) -> None:
        while objects['claim'].tap_if_found():
            print("claimed something")
        sleep(0.5)

    @staticmethod
    def lord_skills() -> None:
        print("lord skills...")
        objects["lord"].tap()
        objects["harvest"].tap(delay=0.5)
        objects["use"].tap(delay=0.5)
        print("harvested. recalling...")
        objects["recall_all"].tap()
        objects["use"].tap(delay=0.5)
        objects["close"].tap(delay=1, repeat=2)
        print("lord skills done.")
    
    @staticmethod
    def heal() -> None:
        if objects["heal"].compare():
            print("healing...")
            objects["heal"].tap()
            objects["go"].tap(delay=1)
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
            objects['go'].tap(delay=1)
            objects['back'].tap(delay=0.5)
        else:
            print("no need to go to sanctuary.")

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
            objects["to_castle"].tap(delay=0.5)

        objects["search"].tap(delay=1, repeat=2)
        while True:
            find_another_mine()
            sleep(1.5)

            match check_status():
                case Status.FOUND:
                    print("Mine found")
                    break
                case Status.NOT_FOUND:
                    if self.mine_type > 0:
                        self.mine_type = MineType(self.mine_type - 1)
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = MineType.IRON
                case Status.NOT_MAP:
                    raise(RuntimeError("Not on the map. Panic."))
                case Status.ERROR:
                    print("some chemistry error")
                
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
                objects["to_castle"].tap(delay=0.5)
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