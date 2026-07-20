from datetime import timedelta
from time import sleep
from typing import Iterator, cast, SupportsInt

from openpyxl import load_workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.formula import DataTableFormula, ArrayFormula
from openpyxl.worksheet.worksheet import Worksheet

from screen_objects import reset_screen, back, screenshot, SwipeSpeed, Direction

from .objects import objects, ScreenObjectNames
from .paths import FARMS_SHEET_PATH
from .status import Status, CastleStatus, MapStatus, MineType, check_map_or_castle, check_castle_status, check_map_status
from .utils import object_from_str

MAX_MINE_LV = 6
ELITE_MINES = range(10)

def cell_assert(cell: Cell, typ: type | tuple[type, type]) -> None:
    val = cell.value
    assert isinstance(val,
                      typ), f"cell at {FARMS_SHEET_PATH} {cell.coordinate} should be {typ.__name__}, got '{val if not isinstance(val, (timedelta, DataTableFormula, ArrayFormula)) else "value doesn't impl repr method"}'"  # type: ignore


class Castle:
    def __init__(self, name: Cell, lv: Cell, google: Cell, account: Cell, alliance: Cell, marches_limit: Cell):
        if lv.value is None:
            lv.value = 1
            save_workbook()

        none_type = type(None)
        cell_assert(name, str)
        cell_assert(lv, SupportsInt)
        cell_assert(google, (SupportsInt, none_type))
        cell_assert(account, (SupportsInt, none_type))
        cell_assert(alliance, (str, none_type))
        cell_assert(marches_limit, (int, none_type))

        self.name_cell = name
        self.google_cell = google
        self.account_cell = account
        self.lv_cell = lv
        self.alliance_cell = alliance
        self.max_marches_cell = marches_limit

        self.mine_lv = MAX_MINE_LV
        self.mine_type: MineType = MineType.IRON
        self.is_enough_troops = True
        self.elite_mines = self.alliances_elite_mines.setdefault(cast(str, alliance.value), iter(ELITE_MINES))

    alliances_elite_mines: dict[str, Iterator[int]] = {}

    @property
    def name(self) -> ScreenObjectNames:
        val = self.name_cell.value
        return cast(ScreenObjectNames, val)

    @name.setter
    def name(self, value: str):
        self.name_cell.value = value
        save_workbook()

    @property
    def lv(self) -> int:
        return int(cast(SupportsInt, self.lv_cell.value))

    @lv.setter
    def lv(self, value: int):
        self.lv_cell.value = value
        save_workbook()

    @property
    def google(self) -> int:
        return int(cast(SupportsInt, self.google_cell.value))

    @google.setter
    def google(self, value: int):
        self.google_cell.value = value
        save_workbook()

    @property
    def account(self) -> int:
        return int(cast(SupportsInt, self.account_cell.value))

    @account.setter
    def account(self, value: int):
        self.account_cell.value = value
        save_workbook()

    @property
    def alliance(self) -> str:
        return cast(str, self.alliance_cell.value)

    @alliance.setter
    def alliance(self, value: str):
        self.alliance_cell.value = value
        save_workbook()

    @property
    def marches(self) -> int:
        cell = self.max_marches_cell
        if cell.value is None:
            objects['lord_info'].tap()
            objects['check_details'].waitap()
            sleep(1)
            for i in reversed(range(4)):
                if object_from_str(f'march_limit_{i}').exists():
                    cell.value = i
                    save_workbook()
                    break
            else:
                screenshot()
                raise RuntimeError("No march num found in march_limit. Check screen.png")
            back()
            sleep(0.3)
            back()
            sleep(0.2)
        return cast(int, cell.value) + 1

    @marches.setter
    def marches(self, value: int):
        self.max_marches_cell.value = value
        save_workbook()

    def new_account(self) -> None:
        if objects['avatar'].tap():
            objects['account'].waitap()
            objects['new_game'].waitap()
            objects['confirm'].waitap()
            objects['realm'].waitap()
            sleep(6)

        objects['man'].wait()
        objects['man'].swipe(Direction.Up, SwipeSpeed.Slow, 1.5)
        objects['man'].swipe(Direction.Right, SwipeSpeed.Slow, 0.6)
        sleep(6)
        objects['man'].swipe(Direction.Up, SwipeSpeed.Slow, 0.8)
        objects['man'].swipe(Direction.Right, SwipeSpeed.Slow, 0.6)

        def kill_monsters():
            while not objects['quest_complete'].tap():
                if objects['blue_bonus'].tap():
                    objects['confirm_bonus'].waitap()
                else:
                    objects['man'].swipe(Direction.Right, SwipeSpeed.Slow, 2)
                    objects['man'].swipe(Direction.Up, SwipeSpeed.Slow, 2)
                    objects['man'].swipe(Direction.Left, SwipeSpeed.Slow, 2)
                    objects['man'].swipe(Direction.Down, SwipeSpeed.Slow, 2)
                reset_screen()
            sleep(1)

        def challenge():
            objects['level'].waitap()
            objects['challenge'].waitap()

        kill_monsters()
        objects['bella'].wait()
        objects['bella'].spam_tap(4, 0.4)
        challenge()  # first level
        kill_monsters()
        print("finished first level")
        objects['bella'].waitap()
        objects['bella'].tap()
        challenge()  # second level
        kill_monsters()
        print("finished second level")
        objects['bella'].waitap()
        objects['bella'].tap()
        objects['backhand'].waitap()
        objects['first_castle'].waitap()
        objects['upgrade'].waitap()
        objects['upgrade_blue'].waitap()
        self.lv = 2
        objects['bella'].waitap()
        objects['bella'].tap()
        objects['monster'].waitap()
        challenge()  # third level
        kill_monsters()
        print("finished third level")
        objects['backhand'].waitap()
        objects['bella'].waitap()
        objects['bella'].tap()
        objects['kingroad'].waitap()
        objects['kingroad_go'].waitap()
        objects['hand'].waitap()
        objects['hand'].waitap()
        objects['upgrade_blue'].waitap()
        objects['kingroad'].waitap()
        self.kingroad_claim()
        self.to_map()
        self.to_castle()
        self.upgrade_castle()
        print("upgraded castle to level 3")
        objects['kingroad'].waitap()
        self.kingroad_claim()
        objects['kingroad_go'].waitap()  # barracks task
        objects['bella'].waitap()
        objects['bella'].tap()
        objects['hand'].waitap()
        objects['hand'].waitap()
        objects['kingroad'].waitap()
        self.kingroad_claim()
        objects['kingroad_go'].waitap()  # savior of order task
        objects['hand'].waitap()
        objects['level'].waitap()  # 4th level
        objects['bright_challenge'].waitap()
        kill_monsters()
        print("finished 4th level")
        objects['bella'].waitap()
        objects['bella'].tap()
        objects['bella'].tap()
        objects['heroic_evolution'].waitap()
        objects['evolve'].waitap()
        back()
        objects['level'].waitap()
        objects['bright_challenge'].waitap()
        kill_monsters()
        print("finished 5th level")
        objects['heroic_evolution'].waitap()
        objects['evolve'].waitap()
        back()
        back()
        self.to_map()
        self.to_castle()
        self.upgrade_castle()
        self.upgrade_castle()

    @staticmethod
    def kingroad_claim():
        if objects['kingroad'].tap():
            sleep(0.8)
        while objects['kingroad_claim'].tap():
            sleep(1)
            back()
            sleep(0.5)
        if objects['kingroad_done'].tap():
            sleep(2)
            back()
            sleep(0.3)

    def log_into_account(self) -> None:
        print(f"checking is current castle: {self.name}")
        if not objects[self.name].exists():
            print(f"logging into {self.name}")

            while True:
                if objects["avatar"].tap():
                    sleep(1)
                if objects["account"].tap():
                    sleep(1)
                if objects["switch"].tap():
                    sleep(1)
                objects["login"].waitap(3)
                if not objects['gmail'].wait(10):
                    back()
                    continue
                objects["gmail"].tap_nth(self.google)
                if not objects["acc_list"].wait(15):
                    back()
                    continue
                is_green = objects['green_castle'].exists()
                if not objects["castle"].tap_nth(self.account - is_green):
                    screenshot()
                    raise RuntimeError(
                        f"cannot log into castle \n name: {self.name} \n google: {self.google} \n account: {self.account} \n check screen.png for more info")
                objects["confirm"].waitap()
                break
            print("logged in.")
            sleep(5)

            while check_castle_status() == CastleStatus.NOT_IN_CASTLE:
                reset_screen()
                sleep(1)
                print("loading...")
                sleep(1)
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
        sleep(1)
        print("ad closed.")

    @classmethod
    def claim(cls) -> None:
        if check_castle_status() == CastleStatus.AD:
            cls.close_ad()
        print(f"claiming {objects['horse'].count()} horses")
        while objects['horse'].tap():
            sleep(0.7)
        if objects['claim'].tap():
            sleep(1)
            back()
            sleep(1)

    @staticmethod
    def lord_skills() -> None:
        print("lord skills...")
        objects["lord"].tap()
        if objects['gather_speed_up'].waitap(2):
            objects['use'].waitap(5)
        objects["harvest"].waitap(3)
        if objects["use"].waitap(2):
            print("harvested")
        objects["recall_all"].waitap(3)
        sleep(0.1)
        if not objects["use"].waitap(2):
            back()
            objects['use'].waitap(2)
        print("lord skills done.")
        reset_screen()
        sleep(0.8)

    @staticmethod
    def heal() -> None:
        if objects['claim_healed'].waitap(0.5):
            print("claimed healed")
            sleep(1)
        if objects["hospital"].waitap(1):
            print("healing...")
            objects["heal"].waitap()
            if objects['confirm_rss'].waitap(1.5):
                sleep(1)
        else:
            print("no need to go to the hospital.")
        objects["ask_help"].waitap(1)
        if objects['sanctuary'].waitap(1.6):
            print("sanctuary...")
            objects['revive'].waitap()
            objects['claim_holy_water'].waitap(1)
            if not objects['confirm_claim_water'].waitap(0.5):
                objects['holy_quest'].waitap(0.5)
                objects['claim_holy_quest'].waitap(1)
                if objects['confirm_claim_water'].waitap(1):
                    sleep(0.5)
                objects['holy_revival'].waitap(0.8)
            objects['revive'].waitap(1)
            sleep(0.3)
            back()
        else:
            print("no need to go to sanctuary.")
        objects['hospital_building'].waitap(0.7)
        if objects['speed_up'].waitap(1.5):
            objects['one-tap_speed_up'].waitap()
            objects["confirm_speed_up"].waitap()
            objects["claim_healed"].waitap()
            sleep(0.5)

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

    def upgrade_castle(self):
        def build_need():
            if objects['upgrade_blue'].tap():
                sleep(0.5)
            else:
                if objects['go_upgrade'].tap():
                    sleep(0.5)
                    build_need()
                else:
                    screenshot()
                    raise RuntimeError("cannot find upgrade buttons. check screen.png")

        objects['castle_building'].waitap()
        objects['upgrade'].waitap()
        sleep(1)
        if self.lv == 2:
            sleep(3)
        if objects['upgrade_blue'].tap():
            self.lv += 1
        else:
            build_need()

    def build(self):
        if self.lv < 15:
            objects['castle_building'].tap()
        else:
            objects['tasks'].tap()
            sleep(0.8)
            objects['build_task'].tap_nth(0)
            sleep(0.5)
            objects['hand'].spam_tap(2, 0.5)
        objects['upgrade'].tap()
        sleep(0.7)
        if not objects['upgrade_blue'].tap():
            objects['go_upgrade'].tap()
            sleep(1)
            objects['upgrade_blue'].tap()

    @staticmethod
    def recruit():
        objects['tasks'].tap()
        sleep(0.8)
        for i in range(objects['recruit_task'].count()):
            objects['recruit_task'].tap_nth(i)
            objects['hand'].waitap()
            objects['recruit'].waitap()
            if objects['x_news'].tap():
                sleep(1)
            objects['cavalry'].waitap()
            sleep(0.8)
            objects['previous'].spam_tap(8, 0.02)
            sleep(0.2)
            objects['second'].tap()
            sleep(0.2)
            if objects['recruit_blue'].tap():
                sleep(0.1)
            back()
            objects['tasks'].waitap()
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

    def free_marches(self) -> int:
        limit = self.marches
        if objects['more_marches'].tap():
            sleep(0.3)
        busy = objects['withdraw'].count() + objects['speed_up_march'].count()
        print(f"free marches: {limit - busy}")
        return limit - busy

    def get_std_mine(self) -> None:
        """Go to standard mine from the map."""

        objects["search"].tap()
        for _ in range(MAX_MINE_LV * MineType.IRON):
            print(f"searching mine. lv {self.mine_lv} {self.mine_type.name.lower()}")
            object_from_str(f"{self.mine_type.name.lower()}_type").waitap()
            objects["plus"].spam_tap(5, 0)
            objects["minus"].spam_tap(6 - self.mine_lv, 0)
            objects["go"].spam_tap(4, 0.1)
            objects['gather'].wait(1.5)

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
                    raise RuntimeError(f"Not at map when searching mine.")
        else:
            screenshot()
            raise RuntimeError(f"cannot find standard mine. check screen.png")

        objects['gather'].tap()
        sleep(0.2)
        objects["gather"].tap()
        objects["set_out"].waitap()
        sleep(0.5)
        if check_map_status() == MapStatus.NOT_AT_MAP:
            back()
            print("not enough horses")
            self.is_enough_troops = False
            sleep(1)
        else:
            print("mine taken.")

    def get_elite_mine(self) -> bool:
        print("Elite")
        for e in self.elite_mines:
            assert (
                       status := check_map_or_castle()) == Status.OUTSIDE, f"unexpected status while getting elite mine: {status}"
            objects["book"].tap()
            if objects['x_news'].waitap(0.5):
                sleep(0.5)
            objects["elite_mines"].tap()
            objects['blue'].wait(1)
            if objects["blue"].tap_nth(e):  # color of blue
                if objects["gather"].waitap(2.5):
                    objects["set_out"].waitap()  # regularly I should be there
                    sleep(0.6)
                    if check_map_status() == MapStatus.NOT_AT_MAP:
                        back()
                        sleep(1)
                    return True
            else:
                print("some chemistry error")
                back()
                return False  # if there is no elites
        raise RuntimeError("all elite mines are full.")


workbook = load_workbook(FARMS_SHEET_PATH)
sheet = workbook.active
if sheet is None:
    raise ValueError("No active sheet in workbook")


def save_workbook() -> None:
    workbook.save(FARMS_SHEET_PATH)


def iter_castles():
    assert isinstance(sheet, Worksheet)

    keys: list[str] = [cell.value for cell in sheet[1] if cell.value is not None]  # type: ignore
    inp = input("enter from which castle do we start: ")  # first row is header

    def check_avatar():
        assert isinstance(sheet, Worksheet)

        for cell in sheet['A'][1:]:
            if not isinstance(cell.value, str):
                raise ValueError(f"castle name {cell.value} is not a string")
            if object_from_str(cell.value).exists():
                return cell.row
        else:
            raise RuntimeError("cannot find any castle on the screen")

    match inp:
        case "":
            start_row = check_avatar()
        case "next":
            start_row = check_avatar() + 1
        case n if n.isdigit():
            start_row = max(int(n), 1) + 1  # because of header
        case name:
            start_row = next(
                i for i, cell in enumerate(sheet['A'][1:], start=2)
                if cell.value == name
            )
    for row in sheet.iter_rows(min_row=start_row):
        kwargs = dict(zip(keys, row))
        yield Castle(**kwargs)
