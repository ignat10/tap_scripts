from time import sleep
from typing import Iterator

import openpyxl
from screen_objects import reset_screen, back

from .objects import objects, ScreenObjectNames
from .status import MineType, Status, check_status
from .paths import FARMS_SHEET_PATH
from .utils import object_from_str




class Castle:
    def __init__(self, name: str, lv: int, google: int, alliance: str):
        self.name: ScreenObjectNames = name.replace('.', '') # type: ignore
        self.google = google
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type: MineType = MineType.IRON

    alliances_elite_mines: dict[str, int] = {}

    @property
    def alliance_mines_num(self) -> int:
        return self.alliances_elite_mines.setdefault(self.alliance, 0)

    @alliance_mines_num.setter
    def alliance_mines_num(self, value: int) -> None:
        self.alliances_elite_mines[self.alliance] = value

    def log_into_account(self) -> None:
        print(f"checking is current castle: {self.name}")
        if not objects[self.name].exists():
            print(f"logging into {self.name}")

            while True:
                if objects["avatar"].tap():
                    sleep(1)
                objects["account"].tap()
                sleep(1)
                objects["switch"].tap()
                sleep(1)
                objects["login"].tap()
                sleep(2)
                if not objects["gmail"].tap_nth(self.google):
                    back()
                    continue
                sleep(3)
                if not objects["castle"].tap_nth(self.account):
                    back()
                    continue
                sleep(1)
                objects["confirm"].tap()
                break
            print("logged in.")
            sleep(5)

            while check_status() == Status.ERROR:
                reset_screen()
                sleep(1)
                print("loading...")
            status = check_status()
            assert(status == Status.INSIDE_AD or status == Status.INSIDE_CLOSED)
            print("loaded.")
        else:
            print(f"already logged into {self.name}")

    @staticmethod
    def close_ad() -> None:
        while check_status() != Status.INSIDE_CLOSED:
            if check_status() != Status.INSIDE_AD:
                raise RuntimeError("I'm not inside the castle.")

            if not (objects['claim_daily'].tap() or objects['x'].tap()):
                back()
            sleep(1.5)
        print("ad closed.")

    @staticmethod
    def lord_skills() -> None:
        print("lord skills...")
        objects["lord"].tap()
        sleep(1.5)
        if objects['gather_speed_up'].tap():
            sleep(0.5)
            objects['use'].tap()
            sleep(0.2)
        objects["harvest"].tap()
        sleep(0.2)
        objects["use"].tap()
        print("harvested")
        objects["recall_all"].tap()
        sleep(0.2)
        if not objects["use"].tap():
            back()
            objects['use'].tap()
        print("lord skills done.")
        sleep(0.3)
    
    @staticmethod
    def heal() -> None:
        if objects['claim_healed'].tap():
            print("claimed healed")
            sleep(1)
        if objects["hospital"].tap():
            print("healing...")
            sleep(1)
            objects["heal"].tap()
            sleep(1)
            objects['confirm_rss'].tap()
            sleep(1)
        objects["ask_help"].tap()
        objects['hospital_building'].tap()
        sleep(1)
        if objects['speed_up'].tap():
            sleep(0.5)
            objects['one-tap_speed_up'].tap()
            sleep(0.5)
            objects["confirm_speed_up"].tap()
            sleep(0.7)
            objects["claim_healed"].tap()
            sleep(0.5)
        if objects['sanctuary'].tap():
            print("sanctuary...")
            sleep(1)
            objects['revive'].tap()
            objects['claim_holy_water'].tap()
            sleep(0.5)
            if not objects['confirm_claim_water'].tap():
                sleep(0.5)
                objects['holy_quest'].tap()
                sleep(0.5)
                objects['claim_holy_quest'].tap()
                sleep(0.5)
                if objects['confirm_claim_water'].tap():
                    sleep(0.5)
                objects['holy_revival'].tap()
            sleep(0.5)
            objects['revive'].tap()
            sleep(0.3)
            back()
        else:
            print("no need to go to sanctuary.")

    @staticmethod
    def go_outside() -> None:
        print("going outside...")
        while not objects['book'].exists():
            if not objects["map"].tap():
                back()
            reset_screen()
            sleep(3)
        print("outside.")

    def get_std_mine(self) -> None:
        """Go to standard mine from the map."""

        objects["search"].tap()
        while True:
            print(f"searching mine. lv {self.mine_lv} {self.mine_type.name.lower()}")
            sleep(0.5)
            object_from_str(f"{self.mine_type.name.lower()}_type").tap()
            objects["plus"].spam_tap(5, 0)
            objects["minus"].spam_tap(6 - self.mine_lv, 0)
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
                case Status.ERROR:
                    print("some chemistry error")
                case status:
                    raise RuntimeError(f"got Status: {status.name} when searching mine.")
                
        objects['gather'].tap()
        sleep(0.2)
        objects["gather"].tap()
        sleep(0.5)
        objects["set_out"].tap()
        print("mine taken.")

    def get_elite_mine(self) -> bool:
        print("Elite")
        while True:
            objects["book"].tap()
            sleep(0.5)
            objects["elite_mines"].tap()
            sleep(1)
            if objects["blue"].tap_nth(self.alliance_mines_num):  # color of blue
                self.alliance_mines_num += 1
                sleep(2)
                if objects["gather_elite"].tap():
                    sleep(0.5)
                    objects["set_out"].tap()  # regularly I should be there
                    sleep(0.2)
                    return True  # everything is alright I went to elite
                else:
                    return self.get_elite_mine()
            else:
                print("some chemistry error")
                back()
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
        try:
            start_row = int(inp) + 1 # because of header
        except ValueError:
            raise ValueError(f"Entered invalid castle number: {inp}")

    for row in sheet.iter_rows(min_row=start_row, values_only=True):
        yield Castle(*row) # type: ignore
