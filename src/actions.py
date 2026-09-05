from datetime import timedelta
from itertools import chain
from random import randrange, choice
from time import sleep, perf_counter
from typing import Iterator, SupportsInt
from typing import cast

from screen_objects import (
    back,
    tap_center,
    swipe_center,
    start_app,
    close_app,
    reset_screen,
    write,
    SwipeSpeed,
    Direction,
    ScreenObject,
)

from src.device import shake
from src.castles import get_column, update_castle
from src.objects import (
    objects,
    ScreenObjectNames,
    bug_levels,
    equipment,
    resources_technology,
    castle_levels,
    resources_need,
    march_limits,
)
from src.paths import CASTLES_DB_PATH
from src.status import CastleStatus, MapStatus, MineType, check_castle_status, check_map_status
from src.utils import log_raise

MAX_MINE_LV = 6
ELITE_MINES = range(10)

directions = (Direction.Up, Direction.Down, Direction.Right, Direction.Left)


def restart_app():
    close_app()
    sleep(4.5)
    start_app()


def value_assert(name: str, value: object, typ: type) -> None:
    val = value
    assert isinstance(val,
                      typ), f"{name} in {CASTLES_DB_PATH} should be {typ.__name__}, got '{val.__repr__() if not isinstance(val, (timedelta, DataTableFormula, ArrayFormula)) else "value doesn't impl repr method"}'"  # type: ignore


class Castle:
    def __init__(self, name: str, lv: int, google: int, account: int | None,
                 alliance: str | None, marches_limit: int | None):

        value_assert("name", name, str)
        value_assert("lv", lv, SupportsInt)
        value_assert("google", google, SupportsInt)
        if account is not None:
            value_assert("account", account, SupportsInt)
        if alliance is not None:
            value_assert("alliance", alliance, str)
        if marches_limit is not None:
            value_assert("marches_limit", marches_limit, SupportsInt)

        self._name = name
        self._google = google
        self._account = account
        self._lv = lv
        self._alliance = alliance
        self._max_marches = marches_limit

        self.has_speed = True
        self.need_rss: MineType | None = None
        self.stamina = True
        self.mine_type = (
            (level, mine)
            for level in [5, 6, 4, 3, 2, 1]
            for mine in MineType
            if mine == MineType.FOOD or mine == MineType.WOOD or (mine == MineType.STONE and self.lv >= 10) or (
                mine == MineType.IRON and self.lv >= 15)
        )
        self.is_enough_troops = True
        self.elite_mines = self.alliances_elite_mines.setdefault(cast(str, alliance), iter(ELITE_MINES))

    alliances_elite_mines: dict[str, Iterator[int]] = {}

    @property
    def name(self) -> ScreenObjectNames:
        return cast(ScreenObjectNames, self._name)

    @property
    def lv(self) -> int:
        return self._lv

    @lv.setter
    def lv(self, value: int):
        update_castle(self._name, "lv", value)
        self._lv = value

    @property
    def google(self) -> int:
        return self._google

    @google.setter
    def google(self, value: int):
        update_castle(self._name, "google", value)
        self._google = value

    @property
    def account(self) -> int | None:
        return int(self._account) if isinstance(self._account, SupportsInt) else None

    @account.setter
    def account(self, value: int):
        update_castle(self._name, "account", value)
        self._account = value

    @property
    def alliance(self) -> str:
        return cast(str, self._alliance)

    @alliance.setter
    def alliance(self, value: str):
        update_castle(self._name, "alliance", value)
        self._alliance = value

    @property
    def marches(self) -> int:
        """gets available marches value. From 1 to 4"""
        val = self._max_marches
        if val is None:
            self.check_marches()
            val = self._max_marches
        assert isinstance(val, int)
        assert 0 <= val <= 3, f"additional marches value must be in range 0..3, got {val}"
        return val + 1

    @marches.setter
    def marches(self, value: int):
        """Set the marches value and persist it in SQLite."""
        update_castle(self._name, "marches_limit", value)
        self._max_marches = value

    @staticmethod
    def close_bella() -> bool:
        if not objects['bella'].exists():
            return False
        while objects['bella'].tap():
            sleep(1.5)
        return True

    def new_account(self) -> None:
        """creates new account, upgrades castle to level 4. from city or map."""
        if self.account is not None:
            return
        if objects['avatar'].tap():
            objects['account'].force_waitap()
            objects['new_game'].force_waitap()
            objects['confirm'].force_waitap()
            objects['realm'].force_waitap()
            print("account created")

        objects['man'].force_wait(100)
        swipe_center(Direction.Up, SwipeSpeed.Slow, 1.7)
        swipe_center(Direction.Right, SwipeSpeed.Slow, 0.75)
        sleep(15)
        swipe_center(Direction.Up, SwipeSpeed.Fast, 0.9)
        swipe_center(Direction.Right, SwipeSpeed.Fast, 0.8)
        self.kill_monsters()
        print("finished 0 level")
        objects['bella'].force_wait(30)
        self.close_bella()
        self._challenge()  # first level
        self.kill_monsters()
        print("finished 1st level")
        sleep(1.5)
        self.close_bella()
        self._challenge()
        self.kill_monsters()
        print("finished 2nd level")
        objects['bella'].force_wait()
        self.close_bella()
        restart_app()
        objects['bella'].force_wait(300)
        self.close_bella()
        objects['first_castle'].force_waitap()
        objects['upgrade'].force_waitap()
        objects['upgrade_blue'].force_waitap()
        self.lv = 2
        objects['bella'].force_wait()
        self.close_bella()
        objects['new_monster'].force_waitap()
        self._challenge()
        self.kill_monsters()
        print("finished 3rd level")
        objects['backhand'].force_waitap()
        objects['bella'].force_wait()
        self.close_bella()
        objects['kingroad'].force_waitap()
        sleep(1.5)
        back()
        self.bind_account()
        self.claim_mail()
        self.change_name()
        print(f"account created, bound, named, upgraded to castle level {self.lv}")

    @classmethod
    def _challenge(cls) -> None:
        for obj in bug_levels:
            obj.tap()
        if not (objects['challenge'].waitap(3) or objects['bright_challenge'].tap()):
            cls._challenge()
            return
        if objects['heroic_evoluation_blue'].waitap(1):
            objects['evolve'].waitap(3)
            back()
            cls._challenge()

    @staticmethod
    def kill_monsters() -> None:
        print("killing monsters")
        while not (objects['quest_complete'].tap() or objects['quit'].tap() or objects['backhand'].exists()):
            if objects['blue_bonus'].tap():
                objects['confirm_bonus'].wait(3)
            if objects['confirm_bonus'].tap():
                sleep(1.2)
            else:
                swipe_center(choice(directions), SwipeSpeed.Slow, 4)
        sleep(1.5)

    def change_name(self) -> None:
        objects['avatar'].force_waitap(3)
        if objects['x_news'].waitap(1.3):
            sleep(1.5)
        objects['change_name'].force_waitap(4)
        sleep(0.9)
        objects['2-16_characters'].force_waitap(5)
        sleep(1.2)
        write(self.name)
        sleep(3)
        objects['change_name_green'].force_waitap(5)
        sleep(1.5)
        if objects['change_name_green'].exists():
            log_raise(f"Name {self.name} already taken.")
        back()
        sleep(0.8)
        print("name has been changed")

    def check_level(self) -> None:
        objects['avatar'].force_tap()
        if not objects['account'].wait(5):
            self.close_ad()
            self.check_level()
            return
        reset_screen()
        sleep(3)
        for level, obj in castle_levels.items():
            if obj.exists():
                self.lv = level
                print(f"saved {self.name} level {level}")
                self.close_ad()
                return
        log_raise("No castle level found.")

    def check_marches(self) -> None:
        objects['lord_info'].force_waitap(5)
        if not objects['check_details'].waitap(5):
            self.close_ad()
            self.check_marches()
            return
        sleep(2)
        for limit, obj in march_limits.items():
            if obj.exists():
                self.marches = limit
                print(f"saved {self.name} 1 + {limit} marches")
                self.close_ad()
                return
        log_raise("No march num found in march_limit.")

    def bind_account(self):
        if self.account is not None:
            return
        gmail = self.google
        objects['avatar'].force_tap()
        objects['account'].force_waitap(3)
        if not objects['undo_bind'].exists():
            objects['bind'].force_waitap(3)
            if objects['gmail'].wait(40):
                objects['gmail'].force_tap_nth(gmail)
        if objects['undo_bind'].wait(50):
            account_number = get_column("google").count(gmail) - 1  # self account
            print(f"bind account {self.name} to {gmail} gmail. save it as account number {account_number}")
            self.account = account_number
        self.close_ad()

    def kingroad_task(self) -> bool:
        self.kingroad_claim()
        print("doing kingroad task")
        if not (objects['kingroad'].tap() or objects['hand'].tap() or objects['kingroad_go'].exists()):
            self.close_ad()
            if not (objects['kingroad'].tap() or objects['hand'].tap()):
                return False
        if not objects['kingroad_go'].wait(3):
            self.close_ad()
            return self.kingroad_task()
        upgrade = objects['start_upgrading'].exists()
        if upgrade:
            print("start upgrading task")
        objects['kingroad_go'].force_waitap(8)
        sleep(0.8)
        self.close_bella()
        if objects['loading'].exists():
            objects['book'].wait()

        while objects['hand'].waitap(1.5):
            if objects['heroic_evoluation_blue'].waitap(0.7):
                objects['evolve'].waitap(5)
            objects['go_blue'].tap()
            objects['free'].tap()
            if objects['kingroad_go'].tap():
                print("tapped kingroad go inside hand loop")
            sleep(1)
            reset_screen()

        while objects['map_hand'].waitap(1):
            objects['arrow'].waitap(1)
        print("no more hands")

        if objects['arrow'].exists():
            self.kill_monster()

        elif objects['check'].exists():
            print("gathering")
            objects['gather'].waitap(10)
            sleep(1.5)
            objects['gather'].waitap(4)
            objects['set_out'].waitap(5)
            back()

        elif objects['alliance_bonuses'].exists():
            print("getting into alliance")
            back()
            sleep(1.5)

        if objects['join'].tap():
            back()
        else:
            objects['apply'].tap_each()

        if objects['unlock'].tap():
            print("beast unlocked")
            sleep(20)

        elif objects['unlock_land'].tap():
            print("unlocked land")
            sleep(0.8)

        elif upgrade and objects['upgrade'].tap():
            sleep(1)
            self._build_need()

        elif objects['forge'].exists():
            self.forge()

        elif objects['go_research'].tap():
            if objects['horseshoes'].waitap(2):
                sleep(0.8)
                objects['research_blue'].waitap(2)

        elif objects['research'].exists():
            if not self.speed_up():
                self.research()

        elif objects['recruit'].tap():
            print("recruiting")
            objects['recruit_blue'].wait(2)
        objects['recruit_blue'].tap()

        if objects['upgrade'].tap():
            print("upgrading")
            sleep(1.05)
        self._build_need()

        if objects['fortify'].tap():
            objects['one-tap_upgrade'].waitap(2)
            objects['use_all'].waitap(3)

        if objects['sell'].tap():
            print("shop")
            sleep(1.5)
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
            sleep(1.5)
            print("killing stragglers")
            self.close_bella()
            objects['suppress'].force_waitap(10)
            objects['set_out'].force_waitap(10)
            self.close_ad()

        if objects['alliance_donate'].tap():
            sleep(1.5)
            objects['donate_blue'].spam_tap(4, 0.6)
            objects['donate_confirm'].waitap(3)

        elif objects['bright_challenge'].exists():
            self._challenge()
            objects['man'].force_wait(20)
        if objects['man'].exists():
            self.kill_monsters()

        self.speed_up()
        self.close_ad()
        return True

    @classmethod
    def kingroad_claim(cls):
        """claims completed kingroad tasks"""
        objects['kingroad'].tap()
        if objects['kingroad_done'].waitap(2):
            print("finished kingroad chapter!")
            sleep(3)
            back()
            sleep(0.45)
        else:
            reset_screen()
            while objects['kingroad_claim'].waitap(0.7):
                print("claimed kingroad task!")
                sleep(1.5)
                back()

    def log_into_account(self) -> None:
        """logs into current account. from city or map."""
        gmail = self.google
        account = self.account
        assert gmail is not None, f"called log_into_account for {self.name}, but google not set in {CASTLES_DB_PATH}"
        assert account is not None, f"called log_into_account for {self.name}, but account not set in {CASTLES_DB_PATH}"
        if not objects[self.name].exists():
            print(f"logging into {self.name}")

            while True:
                if objects['exit_game'].exists():
                    print("invalid token.")
                    restart_app()
                    self.load()
                self.close_ad()
                if objects["avatar"].tap():
                    objects['account'].wait(4)
                if objects["account"].tap():
                    objects['switch'].force_wait(15)
                if objects["switch"].tap():
                    sleep(1.5)
                if not (objects["login"].waitap(3) and objects['gmail'].wait(10)):
                    continue
                objects["gmail"].tap_nth(gmail)
                if not objects["acc_list"].wait(15):
                    continue
                is_green = objects['green_castle'].exists()
                objects["castle"].force_tap_nth(max(account - is_green, 0))
                objects["confirm"].waitap()
                break
            print("logged in.")
            sleep(7.5)
            self.load()
        else:
            print(f"already logged into {self.name}")

    @classmethod
    def load(cls) -> None:
        start = perf_counter()
        if objects['avatar'].exists() or objects['map'].exists():
            return
        print("loading")
        while check_castle_status() == CastleStatus.NOT_IN_CASTLE:
            reset_screen()
            if objects['man'].exists():
                return
            now = perf_counter()
            if now - start > 200:
                print("loading timeout. restart app.")
                restart_app()
                cls.load()
            sleep(1.5)
        sleep(3)
        reset_screen()
        print("loaded.")
        cls.close_ad()

    @classmethod
    def close_ad(cls) -> None:
        """closes ad. from city or map"""
        if check_castle_status() == CastleStatus.CLOSED_AD:
            return
        reset_screen()
        for _ in range(4):
            if check_castle_status() == CastleStatus.CLOSED_AD:
                break
            if cls.close_bella():
                print("closed bella. looking for hand.")
                sleep(1.5)
                while objects['hand'].waitap(1):
                    objects['unlock'].waitap(0.6)
                print("end hand.")
            if objects['exit_game'].exists():
                restart_app()
                cls.load()
            if (
                    objects['continue_game'].tap()
                    or objects['x'].tap()
                    or objects['x_new'].tap()
                    or objects['x_news'].tap()
                    or objects['x_swap'].tap()
                    or objects['claim_daily'].tap()
                    or objects['claim_temple'].tap()
                    or objects['check_beast'].tap()
            ) and check_castle_status() == CastleStatus.CLOSED_AD:
                break
            for _ in range(3):
                back()
                sleep(0.2)
            if objects['no'].waitap(3):
                sleep(1.5)
            else:
                tap_center()
        else:
            restart_app()
            cls.load()

    @staticmethod
    def claim_rss():
        print("shaking")
        shake()
        sleep(5)

    @staticmethod
    def claim_quest():
        if objects['quest'].tap():
            sleep(1.5)
            while objects['daily_quest_claim'].waitap(0.4):
                back()
            while objects['claim_daily_quest'].waitap(0.4):
                back()
            sleep(2.2)
            objects['growth_quest'].tap()
            for _ in range(3):
                while objects['claim_growth_quest'].waitap(3):
                    if not objects['reward'].waitap(10):
                        back()
                        sleep(1.5)
                        back()
                if not objects['another_growth_quest'].waitap(2):
                    break
            back()

    @classmethod
    def claim_mail(cls) -> None:
        objects['mail'].force_tap()
        objects['delete_mail'].waitap(3)
        if objects['mail_reward'].waitap(1):
            objects['read_claim_all'].force_waitap(5)
            objects['confirm_read_all'].force_waitap(5)
            cls.close_ad()
            cls.claim_mail()
        else:
            cls.close_ad()

    @classmethod
    def claim(cls) -> None:
        """claims recruited troops, gift, and RSS. from city"""
        cls.close_ad()
        if objects['horse'].exists():
            print("claiming horses")
            objects['horse'].tap_each()
        if objects['claim'].tap():
            sleep(1.5)
            back()
            sleep(1.5)
        objects['help'].tap()

    @classmethod
    def events(cls):
        def claim_7_march():
            if objects['7-day_march'].tap():
                sleep(1)
                for i in range(objects['!'].count() * 2):
                    objects['event_claim'].tap_each()
                    while not (objects['!'].exists() or objects['event_claim'].exists() or objects['7-day_march'].tap() or objects['map'].exists()):
                        back()
                        sleep(1)
                    sleep(2)
            cls.close_ad()
        def claim_rise():
            if objects['rising_road'].tap():
                sleep(1)
                while objects['event_arrow'].waitap(1):
                    sleep(1.5)
                    back()
                back()

        objects['events'].force_waitap(10)
        sleep(1.5)
        claim_7_march()
        sleep(1.5)
        claim_rise()

    @classmethod
    def upgrade_lord_skills(cls) -> None:
        objects['lord_info'].tap()
        objects['lord_skills'].force_waitap(10)
        objects['development_skills'].force_waitap(10)
        sleep(0.5)
        while not objects['skill_points_0'].exists():
            if objects['upgrade_to_max'].exists():
                break
            while not objects['lord_skill'].waitap(1):
                swipe_center(Direction.Up, SwipeSpeed.Fast, 0.4)
                sleep(1.5)
            objects['upgrade_to_max'].force_waitap(3)
        cls.close_ad()

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
        sleep(0.15)
        if not objects["use"].waitap(2):
            back()
            objects['use'].waitap(2)
        print("lord skills done.")
        reset_screen()
        sleep(1.2)

    def heal(self) -> None:
        """heal troops in hospital and sanctuary, then claim healed. from castle."""
        if objects['claim_healed'].tap():
            print("claimed healed")
            sleep(1.5)
        if objects["hospital"].waitap(0.2):
            print("healing...")
            objects["heal"].waitap()
            if objects['confirm_rss'].waitap(1.5):
                sleep(1.5)
        if objects["ask_help"].waitap(0.2):
            sleep(2.4)
        if objects['sanctuary'].waitap(0.2):
            print("sanctuary...")
            objects['revive'].waitap()
            objects['claim_holy_water'].waitap(1)
            if not objects['confirm_claim_water'].waitap(0.5):
                objects['holy_quest'].waitap(0.5)
                objects['claim_holy_quest'].waitap(1)
                if objects['confirm_claim_water'].waitap(1):
                    sleep(0.8)
                objects['holy_revival'].waitap(0.8)
            objects['revive'].waitap(1)
            sleep(0.5)
            back()
            sleep(1.2)
        if objects['hospital_building'].waitap(0.2):
            sleep(1.5)
        self.speed_up()
        objects['claim_healed'].tap()

    def speed_up(self) -> bool:
        if objects['no_speed'].exists():
            self.has_speed = False
        elif objects['speed_up'].tap() or objects['speed_up_blue'].tap() or objects['get_now'].tap():
            sleep(0.8)
            self.has_speed = False

        if objects['one-tap_speed_up'].tap() and objects["confirm_speed_up"].waitap(3):
            sleep(1.5)
            self.has_speed = True
            return True

        if not self.has_speed:
            print(f"{self.name} has no more speed up.")

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
                sleep(3)
                for techno in resources_technology:
                    if techno.tap():
                        if objects['research_blue'].wait(1.5):
                            break
                        else:
                            back()

        objects['research_blue'].waitap(1)
        back()
        sleep(0.5)
        back()
        sleep(0.5)

    @staticmethod
    def forge() -> None:
        print("forging")
        if objects['forge'].tap():
            sleep(0.8)
        max_item: ScreenObject | None = None
        max_num = 0
        for item in equipment:
            item.force_tap()
            sleep(0.8)
            n = objects['forge_green'].count()
            if n >= max_num:
                max_num = n
                max_item = item
            back()
            sleep(0.8)
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
            sleep(0.5)
        elif objects['upgrade_blue'].tap() or objects['big_upgrade_blue'].tap() or objects['hammer_use'].exists():
            if objects['confirm_rss'].waitap(2):
                return True
            if not (objects['hammer_use'].tap() or objects['hammer_200'].tap()):
                if objects['get_now'].exists():
                    sleep(0.8)
                    self.speed_up()
                else:
                    for need_type, obj in resources_need.items():
                        if obj.exists():
                            self.need_rss = MineType[need_type]
                            print(f"Not enough {need_type} to upgrade.")
                            break
            objects['upgrade_blue'].waitap(1) or objects['big_upgrade_blue'].tap()
        elif objects['go_upgrade'].tap() or objects['hand'].tap():
            sleep(0.8)
            self._build_need()
        else:
            return False
        self.close_ad()
        return True

    def upgrade_castle(self) -> None:
        """upgrades castle or required buildings. from city."""
        objects['castle_building'].waitap()
        objects['upgrade'].waitap()
        sleep(1.5)
        if self.lv == 2:
            sleep(4.5)
        if objects['free'].tap() or objects['upgrade_blue'].tap():
            self.lv += 1
        else:
            self._build_need()

    def build(self) -> bool:
        print("building")
        objects['tasks'].tap()
        objects['build_task'].waitap(2)
        sleep(1.05)
        objects['hand'].waitap(1.5)
        sleep(0.9)
        if objects['upgrade'].tap():
            sleep(1.5)
            return self._build_need()
        else:
            return False

    def recruit(self, *, horses: bool) -> None:
        """recruits horses."""
        print(f"recruiting {"horses" if horses else "powerful troops"}.")
        self.close_ad()
        objects['tasks'].force_tap()
        objects['recruit_task'].wait(1.5)
        barracks = objects['recruit_task'].count()
        back()
        sleep(2)
        for i in range(barracks * 2):
            self.close_ad()
            objects['tasks'].force_waitap(5)
            sleep(1.5)
            objects['recruit_task'].tap_nth(i % barracks)
            sleep(1)
            objects['hand'].waitap(4)
            sleep(1)
            if not objects['recruit'].waitap(3) and objects['free'].tap():
                sleep(1)
                continue
            if objects['x_news'].tap():
                sleep(1.5)
            if horses:
                objects['cavalry'].waitap(3)
                sleep(1.2)
                objects['previous'].spam_tap(8, 0.02)
                sleep(0.3)
                objects['second'].tap()
                sleep(0.3)
            else:
                choice(troops).waitap(3)
                sleep(0.2)
            if not objects['recruit_blue'].waitap(5):
                self.speed_up()
        back()
        sleep(0.5)

    @classmethod
    def use_pack(cls):
        """Uses items from the pack."""
        cls.close_ad()
        objects['pack'].force_tap()
        sleep(1.5)
        for i in range(objects['use_blue'].count()):
            if not objects['use_blue'].wait(5):
                if not objects['pack'].exists():
                    cls.close_ad()
                objects['pack'].force_tap()
            objects['use_blue'].force_wait(5)
            if not objects['use_blue'].tap_nth(i):
                break
            if objects['use_all_items'].waitap(1.5):
                objects['use_all'].force_waitap(10)
                continue
            elif objects['max_items'].tap():
                sleep(0.5)
            objects['use_item'].waitap(1)
        cls.close_ad()

    @classmethod
    def to_map(cls) -> None:
        """Goes to map from inside city"""
        print("going outside...", end=" ")
        while not objects['book'].exists():
            if objects["map"].tap() and objects['loading'].wait(1):
                objects['book'].wait()
                break
            else:
                cls.close_ad()
        sleep(1)
        reset_screen()
        print("outside.")

    def free_marches(self) -> int:
        """get number of available marches of current castle"""
        if check_map_status() == MapStatus.NOT_AT_MAP:
            log_raise("tried to check free marches while not at map")
        limit = self.marches
        if objects['more_marches'].tap():
            sleep(1)
        busy = objects['withdraw'].count() + objects['speed_up_march'].count()
        free = limit - busy
        print(f"available {free}/{limit} marches")
        assert 0 <= free <= limit
        return free

    def kill_monster(self) -> None:
        if not self.stamina:
            return
        self.to_map()
        if objects['search'].tap():
            objects['monster'].force_wait(10)
        if objects['monster'].tap():
        #     objects['plus'].force_wait(10) # FIXME: replace with monster_plus object
        # if objects['plus'].tap():
            objects['go'].force_wait(10)
        objects['go'].spam_tap(5, 0.1)
        if objects['arrow'].wait(2):
            objects['arrow'].force_spam_tap(2, 0.2)
        start = perf_counter()
        while not objects['attack'].waitap(0.5):
            if objects['quick_search'].tap():
                objects['map_hand'].force_waitap(3)
                objects['arrow'].force_wait(3)
                objects['arrow'].spam_tap(2, 0.5)
            else:
                tap_center()
            if perf_counter() - start > 30:
                self.close_ad()
                return
        objects['set_out'].waitap(2)
        if objects['use_stamina'].waitap(1):
            objects['confirm_use_stamina'].force_waitap(3)
            back()
            objects['set_out'].force_waitap(3)
            sleep(1.5)
        if check_map_status() == MapStatus.NOT_AT_MAP:
            self.stamina = False
            back()
            back()

    def get_std_mine(self) -> None:
        """Gets standard mine from the map."""

        if self.free_marches() == 0:
            return

        objects["search"].force_tap()
        need_level = reversed(range(MAX_MINE_LV))
        for _ in range(24):
            level, need_type = (next(need_level), self.need_rss) if self.need_rss is not None else next(self.mine_type)
            print(f"searching mine. lv {level} {need_type.name.lower()}")
            need_type.value.force_waitap(15)
            objects["plus"].spam_tap(5, 0)
            objects["minus"].spam_tap(MAX_MINE_LV - level, 0)
            objects["go"].spam_tap(4, 0.1)
            objects['gather'].wait(4)

            match check_map_status():
                case MapStatus.FOUND:
                    objects['gather'].force_tap()
                    objects["gather"].force_waitap(0.7)
                    objects["set_out"].force_waitap(10)
                    sleep(1)
                    if check_map_status() == MapStatus.NOT_AT_MAP:
                        back()
                        print("not enough horses")
                        self.is_enough_troops = False
                        sleep(1.5)
                    else:
                        print("mine taken.")
                        self.mine_type = chain([(level, need_type)], self.mine_type)
                    break
                case MapStatus.NOT_FOUND:
                    continue
                case MapStatus.NOT_AT_MAP:
                    log_raise(f"Not at map when searching mine.")
        else:
            log_raise(f"cannot find standard mine. check screen.png")
        sleep(1)
        reset_screen()

    def get_elite_mine(self) -> bool:
        """Gets elite mine from the map."""
        blue = next(self.elite_mines, None)
        if blue is None:
            return False

        print("Elite")
        objects["book"].force_tap()

        if objects['x_news'].waitap(0.5):
            sleep(0.8)

        objects["elite_mines"].force_waitap(4)
        sleep(1)
        objects['blue'].wait(3)

        if not objects["blue"].tap_nth(blue):
            back()
            sleep(1)
            return False

        if not objects["gather"].waitap(5):
            return self.get_elite_mine()

        objects["set_out"].force_waitap(5)
        sleep(1.5)

        if check_map_status() == MapStatus.NOT_AT_MAP:
            self.is_enough_troops = False
            back()
            sleep(1.5)

        return True

    def grow(self):
        self.new_account()
        self.log_into_account()
        for i in range(500):
            if i % 60 == 0:
                self.claim_mail()
                self.bind_account()
            if i % 55 == 0:
                self.check_level()
                self.check_marches()
            if i % 50 == 0:
                self.claim_rss()
            if i % 40 == 0:
                self.upgrade_lord_skills()
                self.events()
                self.claim_quest()
                self.use_pack()
            if i % 10 == 1:
                self.kill_monster()
                self.close_ad()
            # if i % 15 == 2:
            #     self.events()
            if i % 20 == 3:
                self.claim_quest()
            self.claim()
            self.heal()
            print("made some task")
            if not self.kingroad_task():
                break

        self.build()
        self.to_map()
        if self.free_marches() != 0:
            if not self.get_elite_mine():
                self.get_std_mine()
        while self.free_marches() >= 1 and self.is_enough_troops:
            self.get_std_mine()

        if not self.is_enough_troops:
            self.close_ad()
            self.recruit()

        print("don't know what to do in this castle.")
