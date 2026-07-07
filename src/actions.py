from time import sleep
from typing import Iterator

import openpyxl
from screen_objects import reset_screen, back

from .objects import objects, ScreenObjectNames
from .status import Status, CastleStatus, MapStatus, MineType, check_map_or_castle, check_castle_status, check_map_status
from .paths import FARMS_SHEET_PATH
from .utils import object_from_str


ELITE_MINES = range(10)

class Castle:
    def __init__(self, name: str, lv: int, google: int, account: int, alliance: str):
        self.name: ScreenObjectNames = name.replace('.', '') # type: ignore
        self.google = google
        self.account = account
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type: MineType = MineType.IRON
        self.elite_mines = self.alliances_elite_mines.setdefault(self.alliance, iter(ELITE_MINES))

    alliances_elite_mines: dict[str, Iterator[int]] = {}

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
                is_green = objects['green_castle'].exists()
                if not objects["castle"].tap_nth(self.account - is_green):
                    back()
                    continue
                sleep(1)
                objects["confirm"].tap()
                break
            print("logged in.")
            sleep(5)

            while check_castle_status() == CastleStatus.NOT_IN_CASTLE:
                reset_screen()
                sleep(1)
                print("loading...")
            print("loaded.")
        else:
            print(f"already logged into {self.name}")

    @staticmethod
    def close_ad() -> None:
        while (status := check_castle_status()) != CastleStatus.CLOSED_AD:
            if status == CastleStatus.NOT_IN_CASTLE:
                for _ in range(5):
                    back()
                    sleep(0.1)
                sleep(1)
                status = check_castle_status()
            if status == CastleStatus.NOT_IN_CASTLE:

                raise RuntimeError(f"Not in castle.")

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
        sleep(0.8)
    
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
        else:
            print("no need to go to the hospital.")
        if not objects["ask_help"].tap():
            objects['hospital_building'].tap()
        sleep(1)
        if objects['speed_up'].tap():
            sleep(0.5)
            objects['one-tap_speed_up'].tap()
            sleep(0.5)
            objects["confirm_speed_up"].tap()
            sleep(1.5)
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
    def to_castle() -> None:
        print("going inside...")
        while check_map_or_castle() != Status.INSIDE:
            back()
        match check_castle_status():
            case CastleStatus.CLOSED_AD:
                return None
            case CastleStatus.AD:
                while check_castle_status() != CastleStatus.CLOSED_AD:
                    back()
                    sleep(1)
            case CastleStatus.NOT_IN_CASTLE:
                raise RuntimeError("Somehow not in castle")

    @staticmethod
    def build():
        objects['tasks'].tap()
        sleep(0.8)
        objects['build_task'].tap_nth(0)
        sleep(0.5)
        objects['hand'].spam_tap(2, 0.5)
        objects['upgrade'].tap()
        sleep(0.7)
        if not objects['upgrade_blue'].tap():
            objects['go_upgrade'].tap()
            objects['upgrade_blue'].tap()

    @staticmethod
    def recruit():
        objects['tasks'].tap()
        sleep(0.8)
        for i in range(objects['recruit_task'].count()):
            objects['recruit_task'].tap_nth(i)
            sleep(1)
            objects['hand'].tap()
            sleep(1.5)
            objects['recruit'].tap()
            sleep(1.5)
            if not objects['recruit_blue'].exists():
                back()
                sleep(0.5)
                objects['tasks'].tap()
                sleep(1)
                continue
            objects['cavalry'].tap()
            sleep(0.8)
            objects['previous'].spam_tap(8, 0.02)
            sleep(0.2)
            objects['second'].tap()
            sleep(0.2)
            objects['recruit_blue'].tap()
            sleep(0.1)
            back()
            sleep(0.5)
            objects['tasks'].tap()
            sleep(1)
        back()
        sleep(0.3)

    @staticmethod
    def to_map() -> None:
        print("going outside...")
        while not objects['book'].exists():
            if not objects["map"].tap():
                back()
            reset_screen()
            sleep(3)
        print("outside.")

    def get_std_mine(self) -> bool:
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

            match check_map_status():
                case MapStatus.FOUND:
                    break
                case MapStatus.NOT_FOUND:
                    if self.mine_type > 1:
                        self.mine_type = MineType(self.mine_type - 1)
                    else:
                        self.mine_lv -= 1
                        self.mine_type = MineType.IRON
                case MapStatus.NOT_AT_MAP:
                    raise RuntimeError(f"Not at when searching mine.")
                
        objects['gather'].tap()
        sleep(0.2)
        objects["gather"].tap()
        sleep(0.5)
        objects["set_out"].tap()
        if check_map_status() == MapStatus.NOT_AT_MAP:
            back()
            sleep(1)
        print("mine taken.")

    def get_elite_mine(self) -> bool:
        print("Elite")
        for e in self.elite_mines:
            assert (status := check_map_or_castle()) == Status.OUTSIDE, f"unexpected status while getting elite mine: {status}"
            objects["book"].tap()
            sleep(0.5)
            objects["elite_mines"].tap()
            sleep(1)
            if objects["blue"].tap_nth(e):  # color of blue
                sleep(2)
                if objects["gather_elite"].tap():
                    sleep(0.5)
                    if not objects["set_out"].tap():  # regularly I should be there
                        back()
                    sleep(0.3)
                    return True
            else:
                print("some chemistry error")
                back()
                return False  # if there is no elites
        raise RuntimeError("all elite mines are full.")

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
