from datetime import timedelta
from time import sleep, perf_counter
from typing import Iterator, SupportsInt
from random import randrange
from itertools import chain
from typing import cast

from openpyxl.cell import Cell
from openpyxl.worksheet.formula import DataTableFormula, ArrayFormula
from keyboard import send, write
from screen_objects import (
    reset_screen,
    back,
    SwipeSpeed,
    Direction,
    tap_center,
    swipe_center,
    start_app,
    close_app,
    ScreenObject
)

from src.objects import (
    ScreenObjectNames,
    objects,
    equipment,
    resources_technology,
    castle_levels,
    resources_need,
)
from src.paths import FARMS_SHEET_PATH
from src.status import Status, CastleStatus, MapStatus, MineType, check_map_or_castle, check_castle_status, check_map_status
from src.worksheet import save_workbook, get_column
from src.utils import object_from_str, log_raise

MAX_MINE_LV = 6
ELITE_MINES = range(10)


def restart_app():
    close_app()
    sleep(3)
    start_app()
    Castle.load()

def shake() -> None:
    send("f9")
    sleep(1.1)
    send("f9")

def cell_assert(cell: Cell, typ: type) -> None:
    val = cell.value
    assert isinstance(val, typ), f"cell at {FARMS_SHEET_PATH} {cell.coordinate} should be {typ.__name__}, got '{val.__repr__() if not isinstance(val, (timedelta, DataTableFormula, ArrayFormula)) else "value doesn't impl repr method"}'"  # type: ignore


class Castle:
    def __init__(self, name: Cell, lv: Cell, google: Cell, account: Cell, alliance: Cell, marches_limit: Cell):
        if lv.value is None:
            lv.value = 1
            save_workbook()

        cell_assert(name, str)
        cell_assert(lv, SupportsInt)
        if google.value is not None:
            cell_assert(google, SupportsInt)
        if account.value is not None:
            cell_assert(account, SupportsInt)
        if alliance.value is not None:
            cell_assert(alliance, str)
        if marches_limit.value is not None:
            cell_assert(marches_limit, SupportsInt)

        self.name_cell = name
        self.google_cell = google
        self.account_cell = account
        self.lv_cell = lv
        self.alliance_cell = alliance
        self.max_marches_cell = marches_limit

        self.has_speed = True
        self.need_rss: MineType | None = None
        self.stamina = True
        self.mine_type = (
            (level, mine)
            for level in [5, 6, 4, 3, 2, 1,]
            for mine in MineType
            if mine == MineType.FOOD or mine == MineType.WOOD or (mine == MineType.STONE and self.lv >= 10) or (mine == MineType.IRON and self.lv >= 15)
        )
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
    def google(self) -> int | None:
        return cast(int | None, self.google_cell.value)

    @google.setter
    def google(self, value: int):
        self.google_cell.value = value
        save_workbook()

    @property
    def account(self) -> int | None:
        return int(val) if isinstance(val := self.account_cell.value, SupportsInt) else None

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
        """gets available marches value. From 1 to 4"""
        cell = self.max_marches_cell
        val = cell.value
        if val is None:
            self.check_marches()
            val = cell.value
        assert isinstance(val, int)
        assert 0 <= val <= 3, f"additional marches value must be in range 0..3, got {val}"
        return val + 1

    @marches.setter
    def marches(self, value: int):
        """sets marches value and saves to .xlsx"""
        self.max_marches_cell.value = value
        save_workbook()

    @staticmethod
    def close_bella() -> bool:
        if not objects['bella'].exists():
            return False
        while objects['bella'].tap():
            sleep(1)
        return True

    def new_account(self) -> None:
        """creates new account, upgrades castle to level 4. from city or map."""
        if objects['avatar'].tap():
            objects['account'].waitap()
            objects['new_game'].waitap()
            objects['confirm'].waitap()
            objects['realm'].waitap()
            print("account created")
            sleep(6)

        objects['man'].wait()
        objects['man'].swipe(Direction.Up, SwipeSpeed.Slow, 1.5)
        objects['man'].swipe(Direction.Right, SwipeSpeed.Slow, 0.6)
        sleep(6)
        objects['man'].swipe(Direction.Up, SwipeSpeed.Slow, 0.8)
        objects['man'].swipe(Direction.Right, SwipeSpeed.Slow, 0.6)
        self.kill_monsters()
        print("finished 0 level")
        objects['bella'].force_wait(15)
        self.close_bella()
        self._challenge()  # first level
        self.kill_monsters()
        print("finished 1st level")
        sleep(1)
        self.close_bella()
        self._challenge()
        self.kill_monsters()
        print("finished 2nd level")
        objects['bella'].force_wait()
        self.close_bella()
        objects['backhand'].force_waitap()
        objects['first_castle'].force_waitap()
        objects['upgrade'].force_waitap()
        objects['upgrade_blue'].force_waitap()
        self.lv = 2
        objects['bella'].force_wait(15)
        self.close_bella()
        objects['new_monster'].force_waitap()
        self._challenge()
        self.kill_monsters()
        print("finished 3rd level")
        objects['backhand'].force_waitap()
        sleep(1)
        self.close_bella()
        objects['kingroad'].force_waitap(20)
        back()
        self.bind_account()
        self.change_name()
        print(f"account created, bound, named, upgraded to castle level {self.lv}")

    @classmethod
    def _challenge(cls) -> None:
        print("challenging")
        if not objects['level'].waitap(2):
            objects['hand'].tap()
        if not objects['challenge'].waitap(3):
            objects['bright_challenge'].force_waitap()
        if objects['heroic_evoluation_blue'].waitap(1):
            objects['evolve'].waitap(3)
            back()
            cls._challenge()

    @staticmethod
    def kill_monsters() -> None:
        def bonus_or(direction: Direction):
            if objects['blue_bonus'].tap():
                sleep(0.8)
            if objects['confirm_bonus'].tap():
                sleep(0.8)
            swipe_center(direction, SwipeSpeed.Slow, 4)
            reset_screen()
        while not (objects['quest_complete'].tap() or objects['quit'].tap()):
            bonus_or(Direction.Right)
            bonus_or(Direction.Up)
            bonus_or(Direction.Left)
            bonus_or(Direction.Down)
            reset_screen()
        sleep(1)

    def change_name(self) -> None:
        objects['avatar'].force_waitap(3)
        if objects['x_news'].waitap(1.3):
            sleep(1)
        objects['change_name'].force_waitap(4)
        objects['2-16_characters'].force_waitap(5)
        sleep(0.8)
        write(self.name)
        sleep(2)
        objects['change_name_green'].force_waitap(5)
        sleep(1)
        if objects['change_name_green'].exists():
            log_raise(f"Name {self.name} already taken.")
        back()
        sleep(0.5)
        print("name has been changed")

    def check_level(self) -> None:
        objects['avatar'].tap()
        objects['account'].force_wait(5)
        reset_screen()
        sleep(2)
        for level, obj in castle_levels.items():
            if obj.exists():
                self.lv = level
                print(f"saved self level {level}")
                back()
                sleep(0.2)
                return
        log_raise("No castle level found.")

    def check_marches(self) -> None:
        objects['lord_info'].force_waitap(5)
        objects['check_details'].force_waitap(5)
        sleep(1)
        for i in reversed(range(4)):
            if object_from_str(f'march_limit_{i}').exists():
                self.marches = i
                save_workbook()
                break
        else:
            log_raise("No march num found in march_limit.")
        back()
        sleep(0.3)
        back()
        sleep(0.2)

    def bind_account(self):
        gmail = self.google
        assert gmail is not None, f"google not set for {self.name}. Please set it manually in {FARMS_SHEET_PATH}."
        while True:
            object_from_str(self.name).force_tap()
            objects['account'].force_waitap(3)
            objects['bind'].force_waitap(3)
            while not objects['gmail'].wait(15):
                objects['bind'].tap()
            objects['gmail'].force_tap_nth(gmail)
            if objects['undo_bind'].wait(3):
                break
            restart_app()
            self.close_ad()
        account_number = get_column("google").count(gmail) - 1 # self account
        print(f"bind account {self.name} to {gmail} gmail. save it as account number {account_number}")
        self.account = account_number
        back()
        back()
        sleep(0.7)

    def kingroad_task(self) -> None:
        self.kingroad_claim()
        if not objects['kingroad'].tap():
            objects['hand'].tap()
        sleep(1)
        upgrade = objects['start_upgrading'].exists()
        if objects['kingroad_go'].waitap(8):
            sleep(0.5)
            self.close_bella()
            if objects['loading'].exists():
                objects['book'].wait()
            while objects['hand'].waitap(1) or objects['map_hand'].tap():
                print("tapped hand")
                if objects['heroic_evoluation_blue'].waitap(0.7):
                    objects['evolve'].waitap(5)
                objects['go_blue'].tap()
                objects['free'].tap()
                if objects['kingroad_go'].tap():
                    print("tapped kingroad go inside hand loop")

            print("no more hands")
            reset_screen()
            if objects['arrow'].exists():
                self.kill_monster()

            elif objects['check'].exists():
                print("gathering")
                objects['gather'].waitap(10)
                sleep(1)
                objects['gather'].waitap(4)
                objects['set_out'].waitap(5)
                back()

            elif objects['alliance_bonuses'].exists():
                print("getting into alliance")
                back()
                sleep(1)

            if objects['join'].tap():
                back()
            else:
                objects['apply'].tap_each()

            if objects['bright_challenge'].exists():
                self._challenge()
                objects['man'].force_wait(20)
            if objects['man'].exists():
                self.kill_monsters()

            if objects['unlock'].tap():
                print("beast unlocked")
                sleep(20)

            elif objects['unlock_land'].tap():
                print("unlocked land")
                sleep(0.5)

            elif upgrade and objects['upgrade'].tap():
                self._build_need()

            elif objects['forge'].exists():
                self.forge()

            elif objects['go_research'].tap():
                if objects['horseshoes'].waitap(2):
                    sleep(0.5)
                    objects['research_blue'].waitap(2)

            elif objects['research'].exists():
                if not self.speed_up():
                    self.research()

            elif objects['recruit'].tap():
                print("recruiting")
                objects['recruit_blue'].wait(2)
            objects['recruit_blue'].waitap(2)

            if objects['upgrade'].tap():
                print("upgrading")
                sleep(0.7)
            self._build_need()

            if objects['fortify'].tap():
                objects['one-tap_upgrade'].waitap(2)
                objects['use_all'].waitap(3)

            if objects['sell'].tap():
                print("shop")
                sleep(1)
                objects['shell'].tap_each()
                objects['buy'].waitap(2)
                for i in range(objects['shell'].count()):
                    objects['shell'].wait()
                    objects['shell'].tap_nth(i)
                    if objects['confirm_shell'].waitap(1):
                        break
                back()

            if not objects['green'].tap():
                if objects['switch_level'].tap():
                    for _ in range(4):
                        objects['green'].force_tap_nth(randrange(15))

            if objects['stragglers'].tap():
                sleep(1)
                print("killing stragglers")
                self.close_bella()
                objects['suppress'].force_waitap(10)
                objects['set_out'].force_waitap(10)
                self.close_ad()

            if objects['alliance_donate'].tap():
                sleep(1)
                objects['donate_blue'].spam_tap(4, 0.6)
                objects['donate_confirm'].waitap(3)

            self.speed_up()
            self.close_ad()

    @classmethod
    def kingroad_claim(cls):
        """claims completed kingroad tasks"""
        objects['kingroad'].tap()
        if objects['kingroad_done'].waitap(1):
            print("finished kingroad chapter!")
            sleep(2)
            back()
            sleep(0.3)
            cls.close_ad()
        else:
            reset_screen()
            while objects['kingroad_claim'].waitap(0.7):
                print("claimed kingroad task!")
                sleep(1)
                back()

    def log_into_account(self) -> None:
        """logs into current account. from city or map."""
        gmail = self.google
        assert gmail is not None, f"called log_into_account for {self.name}, but google not set in {FARMS_SHEET_PATH}"
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
                objects["gmail"].tap_nth(gmail)
                if not objects["acc_list"].wait(15):
                    back()
                    continue
                is_green = objects['green_castle'].exists()
                objects["castle"].force_tap_nth(max(self.account - is_green, 0))
                objects["confirm"].waitap()
                break
            print("logged in.")
            sleep(5)
            self.load()
        else:
            print(f"already logged into {self.name}")

    @staticmethod
    def load():
        start = perf_counter()
        while check_castle_status() == CastleStatus.NOT_IN_CASTLE:
            reset_screen()
            now = perf_counter()
            if now - start > 200:
                print("loading timeout. restart app.")
                restart_app()
                start = perf_counter()
            print("loading...")
            sleep(1)
        print("loaded.")

    @classmethod
    def close_ad(cls) -> None:
        """closes ad. from city or map"""
        if check_castle_status() == CastleStatus.CLOSED_AD:
            return
        reset_screen()
        while check_castle_status() != CastleStatus.CLOSED_AD:
            if cls.close_bella():
                print("closed bella. looking for hand.")
                sleep(1)
                while objects['hand'].waitap(1):
                    sleep(0.5)
                print("end hand.")
            objects['continue_game'].tap()
            objects['x'].tap()
            objects['x_new'].tap()
            objects['x_news'].tap()
            objects['claim_daily'].tap()
            objects['check_beast'].tap()
            if check_castle_status() == CastleStatus.CLOSED_AD:
                break
            else:
                for _ in range(3):
                    back()
                    sleep(0.1)
                sleep(0.6)
            if objects['no'].tap():
                sleep(1)
            if check_castle_status() == CastleStatus.CLOSED_AD:
                break
            if objects['frozen_screen'].exists():
                restart_app()
            else:
                tap_center()
            objects['map'].wait(0.4)
        print("ad closed.")

    @staticmethod
    def claim_rss():
        shake()
        sleep(3)

    @staticmethod
    def claim_quest():
        if objects['quest'].tap():
            sleep(1)
            while objects['daily_quest_claim'].waitap(0.4):
                back()
            while objects['claim_daily_quest'].waitap(0.4):
                back()
            sleep(1.5)
            objects['growth_quest'].tap()
            for _ in range(3):
                while objects['claim_growth_quest'].waitap(3):
                    if not objects['reward'].waitap(10):
                        back()
                        sleep(1)
                        back()
                if not objects['another_growth_quest'].waitap(2):
                    break
            back()

    @classmethod
    def claim_mail(cls) -> None:
        objects['mail'].tap()
        while objects['mail_reward'].waitap(1):
            objects['read_claim_all'].force_waitap(5)
            objects['confirm_read_all'].force_waitap(5)
            cls.close_ad()
            objects['mail'].waitap(3)
        cls.close_ad()

    def claim(self) -> None:
        """claims recruited troops, gift, and RSS. from city"""
        self.close_ad()
        if objects['horse'].exists():
            print("claiming horses")
            objects['horse'].tap_each()
        if objects['claim'].tap():
            sleep(1)
            back()
            sleep(1)
        objects['help'].tap()

    @staticmethod
    def events():
        if objects['events'].waitap(1):
            sleep(1)
        for n in range(objects['event'].count()):
            objects['event'].tap_nth(n)
            sleep(1)
            objects['event_claim'].tap_each()
            for i in range(objects['!'].count()):
                objects['!'].tap_nth(i)
                sleep(0.5)
                def claims():
                    count = objects['event_claim'].count()
                    objects['event_claim'].tap_each()
                    sleep(1)
                    for _ in range(count):
                        back()
                        sleep(0.3)
                claims()
                claims()
            while objects['event_arrow'].tap():
                sleep(1)
            back()
            sleep(0.5)

    @staticmethod
    def upgrade_lord_skills():
        objects['lord_info'].tap()
        objects['lord_skills'].force_waitap(3)
        objects['development_skills'].force_waitap(3)
        sleep(0.3)
        while not objects['skill_points_0'].exists():
            if objects['upgrade_to_max'].exists():
                back()
                sleep(0.3)
                break
            while not objects['lord_skill'].waitap(1):
                swipe_center(Direction.Up, SwipeSpeed.Fast, 0.4)
                sleep(1)
            objects['upgrade_to_max'].force_waitap(3)
        back()
        sleep(0.3)
        back()
        sleep(0.2)

    @staticmethod
    def use_lord_skills() -> None:
        """use lord skills, harvest, gather speed up, recall all. from city or map"""
        print("lord skills...")
        objects["lord"].tap()
        if objects['gather_speed_up'].waitap(2):
            objects['use'].waitap(2)
        if objects["harvest"].waitap(2):
            objects["use"].waitap(2)
        objects["recall_all"].waitap(3)
        sleep(0.1)
        if not objects["use"].waitap(2):
            back()
            objects['use'].waitap(2)
        print("lord skills done.")
        reset_screen()
        sleep(0.8)

    def heal(self) -> None:
        """heal troops in hospital and sanctuary, then claim healed. from castle."""
        if objects['claim_healed'].tap():
            print("claimed healed")
            sleep(1)
        if objects["hospital"].waitap(0.2):
            print("healing...")
            objects["heal"].waitap()
            if objects['confirm_rss'].waitap(1.5):
                sleep(1)
        if objects["ask_help"].waitap(0.2):
            sleep(1.6)
        if objects['sanctuary'].waitap(0.2):
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
            sleep(0.8)
        if objects['hospital_building'].waitap(0.2):
            sleep(1)
        self.speed_up()
        objects['claim_healed'].tap()

    def speed_up(self) -> bool:
        if objects['no_speed'].exists():
            self.has_speed = False
        elif objects['speed_up'].tap() or objects['speed_up_blue'].tap() or objects['get_now'].tap():
            sleep(0.5)
            self.has_speed = False
        if objects['one-tap_speed_up'].tap() and objects["confirm_speed_up"].waitap(3):
            sleep(1)
            self.has_speed = True
            return True
        else:
            if not self.has_speed:
                print(f"castle {self.name} has no more speed up.")
            self.close_ad()
            return False

    def research(self) -> None:
        marches = self.marches
        if not objects['research'].tap():
            if not objects['college'].tap() and objects['research'].waitap(1):
                self.to_map()
                self.close_ad()
            objects['college'].force_tap()
            objects['research'].force_waitap(3)
        match marches, self.lv:
            case 1, lv if lv >= 5:
                print("unlocking 2nd march")
                objects['military'].waitap()
                if not objects['legion'].waitap(1.5):
                    if not objects['expansion'].tap():
                        objects['draft'].force_tap()
            case 2, lv if lv >= 12:
                    print("unlocking 3rd march")
                    objects['military'].waitap()
                    swipe_center(Direction.Up, SwipeSpeed.Normal, 1)
                    if not objects['legion'].waitap(1.5):
                        if not objects['leadership'].tap():
                            objects['horseshoes'].force_tap()
            case 3, lv if lv >= 19:
                    print("unlocking 4th march")
                    objects['military'].waitap()
                    swipe_center(Direction.Up, SwipeSpeed.Turbo, 0.7)
                    if not objects['legion'].waitap(1.5):
                        if not objects['horseshoes'].tap():
                            if not objects['expansion'].tap():
                                objects['draft'].force_tap()
            case _:
                print("researching resources technology.")
                objects['resources'].force_waitap(3)
                sleep(1)
                for techno in resources_technology:
                    techno.waitap(3)
                    if objects['research_blue'].wait(1.5):
                        break
                    else:
                        back()

        objects['research_blue'].waitap(1)
        back()
        sleep(0.3)
        back()
        sleep(0.3)

    @staticmethod
    def forge():
        print("forging")
        if objects['forge'].tap():
            sleep(0.5)
        max_item: ScreenObject | None = None
        max_num = 0
        for item in equipment:
            item.tap()
            sleep(0.5)
            n = objects['forge_green'].count()
            if n >= max_num:
                max_num = n
                max_item = item
            back()
            sleep(0.5)
        if max_item is not None:
            max_item.tap()
            objects['forge_green'].wait(10)
            objects['forge_green'].tap_nth(max_num - 1)
            if objects['+'].waitap(1):
                objects['select'].waitap(3)
            objects['forge_blue'].waitap(1)
            back()
            back()
            back()

    def _build_need(self) -> bool:
        """builds required for upgrade buildings. from upgrade menu."""
        reset_screen()
        if objects['free'].tap():
            print("built for free.")
            sleep(0.3)
        elif objects['upgrade_blue'].tap() or objects['big_upgrade_blue'].tap() or objects['hammer_use'].exists():
            if objects['confirm_rss'].waitap(2):
                return True
            if not (objects['hammer_use'] or objects['hammer_200'].tap()):
                if objects['get_now'].exists():
                    sleep(0.5)
                    self.speed_up()
                else:
                    for name, obj in resources_need.items():
                        if obj.exists():
                            self.need_rss = MineType[name.upper()]
                            print(f"Not enough {name}")
                            break
            objects['upgrade_blue'].waitap(1) or objects['big_upgrade_blue'].tap()
        elif objects['go_upgrade'].tap() or objects['hand'].tap():
            sleep(0.5)
            self._build_need()
        else:
            return False
        self.close_ad()
        return True

    def upgrade_castle(self) -> None:
        """upgrades castle or required buildings. from city."""
        objects['castle_building'].waitap()
        objects['upgrade'].waitap()
        sleep(1)
        if self.lv == 2:
            sleep(3)
        if objects['free'].tap() or objects['upgrade_blue'].tap():
            self.lv += 1
        else:
            self._build_need()

    def build(self) -> bool:
        print("building")
        objects['tasks'].tap()
        objects['build_task'].waitap(2)
        sleep(0.7)
        objects['hand'].waitap(1.5)
        sleep(0.6)
        if objects['upgrade'].tap():
            sleep(1)
            return self._build_need()
        else:
            return False

    def recruit(self) -> None:
        """recruits horses. from the city."""
        print("recruiting")
        objects['tasks'].tap()
        sleep(0.8)
        for i in range(objects['recruit_task'].count()):
            objects['recruit_task'].tap_nth(i)
            objects['hand'].waitap(4)
            objects['recruit'].waitap(4)
            if objects['x_news'].tap():
                sleep(1)
            objects['cavalry'].waitap(3)
            sleep(0.8)
            objects['previous'].spam_tap(8, 0.02)
            sleep(0.2)
            objects['second'].tap()
            sleep(0.2)
            if not objects['recruit_blue'].tap():
                self.speed_up()
            back()
            objects['tasks'].waitap(5)
            sleep(1)
        back()
        sleep(0.3)

    @classmethod
    def to_map(cls) -> None:
        """Goes to map from inside city"""
        print("going outside...")
        while not objects['book'].exists():
            if objects["map"].tap() and objects['loading'].wait(1):
                objects['book'].wait()
                break
            else:
                cls.close_ad()
        print("outside.")

    def free_marches(self) -> int:
        """get number of available marches of current castle"""
        limit = self.marches
        if objects['more_marches'].tap():
            sleep(0.3)
        busy = objects['withdraw'].count() + objects['speed_up_march'].count()
        print(f"free marches: {limit - busy}")
        return limit - busy

    def kill_monster(self) -> None:
        if not self.stamina:
            return
        self.to_map()
        if objects['search'].tap():
            objects['monster'].force_wait(10)
        if objects['monster'].tap():
            objects['go'].force_wait(10)
        if objects['go'].tap():
            objects['arrow'].force_wait(10)
        objects['arrow'].spam_tap(2, 0.2)
        while not objects['attack'].waitap(0.5):
            if objects['quick_search'].tap():
                objects['map_hand'].force_waitap(3)
                objects['arrow'].force_wait(3)
                objects['arrow'].spam_tap(2, 0.5)
            else:
                tap_center()
        objects['set_out'].force_waitap(2)
        if objects['use_stamina'].waitap(1  ):
            objects['confirm_use_stamina'].force_waitap(3)
            back()
            objects['set_out'].force_waitap(3)
            sleep(1)
        if check_map_status() == MapStatus.NOT_AT_MAP:
            self.stamina = False
            back()
            back()

    def get_std_mine(self) -> None:
        """Gets standard mine from the map."""

        objects["search"].force_tap()
        need_level = reversed(range(MAX_MINE_LV))
        for _ in range(24):
            level, need_type = (next(need_level), self.need_rss) if self.need_rss is not None else next(self.mine_type)
            type_name = need_type.name.lower()
            print(f"searching mine. lv {level} {type_name}")
            object_from_str(f"{type_name}_type").waitap()
            objects["plus"].spam_tap(5, 0)
            objects["minus"].spam_tap(MAX_MINE_LV - level, 0)
            objects["go"].spam_tap(4, 0.1)
            objects['gather'].wait(2)

            match check_map_status():
                case MapStatus.FOUND:
                    objects['gather'].force_tap()
                    objects["gather"].force_waitap(0.7)
                    objects["set_out"].force_waitap(5)
                    sleep(0.5)
                    if check_map_status() == MapStatus.NOT_AT_MAP:
                        back()
                        print("not enough horses")
                        self.is_enough_troops = False
                        sleep(1)
                    else:
                        print("mine taken.")
                        self.mine_type = chain([(level, need_type)], self.mine_type)
                    return
                case MapStatus.NOT_AT_MAP:
                    log_raise(f"Not at map when searching mine.")
        else:
            log_raise(f"cannot find standard mine. check screen.png")

    def get_elite_mine(self) -> bool:
        """Gets elite mine from the map."""
        print("Elite")
        for e in self.elite_mines:
            assert (status := check_map_or_castle()) == Status.OUTSIDE, f"unexpected status while getting elite mine: {status}"
            objects["book"].tap()
            if objects['x_news'].waitap(0.5):
                sleep(0.5)
            objects["elite_mines"].force_waitap(4)
            objects['blue'].wait(2)
            if objects["blue"].tap_nth(e):  # color of blue
                if objects["gather"].waitap(2.5):
                    objects["set_out"].force_waitap(5)  # regularly I should be there
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
