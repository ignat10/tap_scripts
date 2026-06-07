from time import sleep
from enum import IntEnum
from typing import Iterator

import openpyxl
from screen_objects import reset_screen, back

from .objects import objects, ScreenObjectNames
from .status import Status, check_status
from .paths import FARMS_SHEET_PATH
from .utils import object_from_str


class MineType(IntEnum):
    FOOD = 1
    WOOD = 2
    STONE = 3
    IRON = 4


class Castle:
    def __init__(self, name: str, lv: int, google: int, alliance: str):
        self.name: ScreenObjectNames = name.replace('.', '') # type: ignore
        self.google = google
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type: MineType = MineType.IRON

    def log_into_account(self) -> None:
        print(f"checking is current castle: {self.name}")
        if not objects[self.name].exists():
            print(f"logging into {self.name}")
            objects["avatar"].tap()
            sleep(0.5)
            objects["account"].tap()
            while True:
                sleep(1)
                objects["switch"].tap()
                sleep(1)
                objects["login"].tap()
                sleep(2)
                if not object_from_str(f"google_{self.google}").tap():
                    back()
                    continue
                sleep(3)
                if not object_from_str(f"{self.name}_account").tap():
                    back()
                    continue
                sleep(1)
                objects["confirm"].tap()
                break
            print("logged in.")
            while not any((
                objects["map"].exists(),
                objects[self.name].exists(),
                objects['x1'].tap(),
                objects["claim_daily"].tap(),
                objects['blur_map'].exists(),
            )):
                reset_screen()
                sleep(1)
                print("loading...")
            print("loaded.")
        else:
            print(f"already logged into {self.name}")

    @staticmethod
    def close_ad() -> None:
        while not objects["map"].exists():
            if not objects["x1"].tap():
                back()
            sleep(1)
        print("ad closed.")

    @staticmethod
    def claim() -> None:
        if objects["claim_healed"].tap():
            print("claimed healed troops")

    @staticmethod
    def lord_skills() -> None:
        print("lord skills...")
        objects["lord"].tap()
        sleep(1)
        objects["harvest"].tap()
        sleep(0.5)
        objects["use"].tap()
        print("harvested. recalling...")
        objects["recall_all"].tap()
        sleep(0.5)
        objects["use"].tap()
        back()
        print("lord skills done.")
    
    @staticmethod
    def heal() -> None:
        if objects["hospital"].tap():
            print("healing...")
            sleep(1)
            objects["heal"].tap()
            sleep(0.5)
            objects['confirm_rss'].tap()
        else:
            print("no need to heal.")
    
        if objects['sanctuary'].exists():
            print("sanctuary...")
            objects['sanctuary'].tap()
            sleep(1)
            objects['heal'].tap()
            back()
        else:
            print("no need to go to sanctuary.")

    @staticmethod
    def go_outside() -> None:
        print("going outside...")
        objects["map"].tap()
        sleep(3)
        print("outside.")

    def get_std_mine(self) -> None:
        """Go to standard mine from the map."""

        objects["search"].tap()
        while True:
            print(f"searching mine. lv {self.mine_lv} {self.mine_type.name.lower().capitalize()}")
            sleep(0.5)
            object_from_str(f"{self.mine_type.name.lower()}_type").tap()
            objects["minus"].spam_tap(5, 0)
            objects["plus"].spam_tap(self.mine_lv - 1, 0)
            objects["go"].spam_tap(4, 0.1)
            sleep(1.5)

            match check_status():
                case Status.FOUND:
                    break
                case Status.NOT_FOUND:
                    if self.mine_type > 1:
                        self.mine_type = MineType(self.mine_type - 1)
                    else:
                        self.mine_lv -= 1
                        self.mine_type = MineType.IRON
                case Status.NOT_MAP:
                    raise(RuntimeError("Not on the map. Panic."))
                case Status.ERROR:
                    print("some chemistry error")
                
        sleep(0.5)
        objects['gather'].tap()
        sleep(0.2)
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
            objects["elite_mines"].tap()
            sleep(1)
            if objects["blue"].tap():  # color of blue
                sleep(2)
                objects["gather_elite"].tap()
                sleep(0.5)
                objects["go"].tap()  # regularly I should be there
                sleep(0.5)
                objects["to_castle"].tap()
                self.alliances_elite_mines[self.alliance] += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                objects["back"].tap()
                return False  # if there is no elites


def iter_castles() -> Iterator[Castle]:
    sheet = openpyxl.load_workbook(FARMS_SHEET_PATH).active
    if sheet is None:
        raise ValueError("cannot load sheet")
    
    inp = input("enter from which castle do we start: ") # first row is header

    if not inp:
        for cell in sheet['A'][1:]:
            if objects[cell.value.replace('.', '')].exists():
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