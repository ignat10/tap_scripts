from datetime import datetime, timedelta
from functools import cached_property
from itertools import chain
from random import randrange, choice, sample
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
    ScreenObjectName,
    bug_levels,
    troops,
    equipment,
    resources_technology,
    castle_levels,
    march_limits,
)
from src.paths import CASTLES_DB_PATH
from src.status import (
    CastleStatus,
    MapStatus,
    MineType,
    Task,
    check_castle_status,
    check_map_status,
)
from src.utils import log_raise

MAX_MINE_LEVEL = 6
MINE_LEVELS_SEQUENCE = [5, 6, 4, 3, 2, 1]
ELITE_MINES = range(10)

SWIPE_DIRECTIONS = (Direction.Up, Direction.Down, Direction.Right, Direction.Left)


def restart_app():
    close_app()
    sleep(4.5)
    start_app()


def value_assert(name: str, value: object, typ: type) -> None:
    val = value
    assert isinstance(
        val, typ
    ), f"{name} in {CASTLES_DB_PATH} should be {typ.__name__}, got '{val.__repr__() if not isinstance(val, (timedelta, DataTableFormula, ArrayFormula)) else "value doesn't impl repr method"}'"  # type: ignore


class Castle:
    def __init__(
        self,
        name: str,
        google: int,
        account: int | None,
        alliance: str | None,
    ):

        value_assert("name", name, str)
        value_assert("google", google, int)
        if account is not None:
            value_assert("account", account, int)
        if alliance is not None:
            value_assert("alliance", alliance, str)
        self._name = name
        self._google = google
        self._account = account
        self._alliance = alliance
        self.no_speed: int = 0
        self.last_gather_at: datetime | None = None
        self.stamina = True
        self.mine_type = (
            (level, mine)
            for level in MINE_LEVELS_SEQUENCE
            for mine in MineType
            if mine == MineType.FOOD
            or mine == MineType.WOOD
            or (mine == MineType.STONE and self.level >= 10)
            or (mine == MineType.IRON and self.level >= 15)
        )
        self.is_enough_troops = True
        self.elite_mines = self.alliances_elite_mines.setdefault(
            cast(str, alliance), iter(ELITE_MINES)
        )

    alliances_elite_mines: dict[str, Iterator[int]] = {}

    @property
    def name(self) -> ScreenObjectName:
        return cast(ScreenObjectName, self._name)

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
    def last_gather_ago(self) -> int | None:
        """Return elapsed gather time: seconds below a minute, otherwise minutes."""
        if self.last_gather_at is None:
            return None

        return int((datetime.now() - self.last_gather_at).total_seconds())

    def set_last_gather_now(self) -> None:
        """Mark gathering as having happened just now."""
        self.last_gather_at = datetime.now()

    @cached_property
    def marches(self) -> int:
        """gets available marches value. From 1 to 4"""
        objects["lord_info"].force_waitap(5)
        if not objects["check_details"].waitap(5):
            self.close_ad()
            return self.marches
        sleep(2)
        for limit, obj in march_limits.items():
            if obj.exists():
                print(f"saved {self.name} 1 + {limit} marches")
                self.close_ad()
                assert (
                    0 <= limit <= 3
                ), f"additional marches value must be in range 0..3, got {limit}"
                return limit + 1
        log_raise("No march num found in march_limit.")

    @staticmethod
    def close_bella() -> bool:
        if not objects["bella"].exists():
            return False
        while objects["bella"].tap():
            sleep(1.5)
        return True

    def new_account(self) -> None:
        """creates new account, upgrades castle to level 4. from city or map."""
        if self.account is not None:
            return
        if objects["avatar"].tap():
            objects["account"].force_waitap()
            objects["new_game"].force_waitap()
            objects["confirm"].force_waitap()
            objects["realm"].force_waitap()
            print("account created")

        objects["man"].force_wait(100)
        swipe_center(Direction.Up, SwipeSpeed.Slow, 1.7)
        swipe_center(Direction.Right, SwipeSpeed.Slow, 0.75)
        sleep(15)
        swipe_center(Direction.Up, SwipeSpeed.Fast, 0.9)
        swipe_center(Direction.Right, SwipeSpeed.Fast, 0.8)
        self.kill_monsters()
        print("finished 0 level")
        objects["bella"].force_wait(30)
        self.close_bella()
        self.challenge()  # first level
        print("finished 1st level")
        sleep(1.5)
        self.close_bella()
        self.challenge()
        print("finished 2nd level")
        objects["bella"].force_wait()
        self.close_bella()
        restart_app()
        objects["bella"].force_wait(300)
        self.close_bella()
        objects["first_castle"].force_waitap()
        objects["upgrade"].force_waitap()
        objects["upgrade_blue"].force_waitap()
        objects["bella"].force_wait()
        self.close_bella()
        objects["new_monster"].force_waitap()
        self.challenge()
        print("finished 3rd level")
        objects["backhand"].force_waitap()
        objects["bella"].force_wait()
        self.close_bella()
        objects["kingroad"].force_waitap()
        sleep(1.5)
        back()
        sleep(1)
        self.bind_account()
        self.claim_mail()
        self.change_name()
        print(f"account created, named and bound")

    @classmethod
    def challenge(cls) -> bool:
        for obj in bug_levels:
            obj.tap()
        if not (objects["challenge"].waitap(3) or objects["bright_challenge"].tap()):
            return False

        if not objects["heroic_evoluation_blue"].waitap(1) and objects["man"].wait(5):
            cls.kill_monsters()
            return True

        objects["evolve"].waitap(3)
        back()
        sleep(1)
        return False

    @classmethod
    def kill_monsters(cls) -> None:
        print("killing monsters")
        for _ in range(50):
            if (
                objects["quest_complete"].tap()
                or objects["quit"].tap()
                or objects["backhand"].exists()
            ):
                break
            elif objects["blue_bonus"].tap():
                objects["confirm_bonus"].wait(3)
            if objects["confirm_bonus"].tap():
                sleep(1.2)
            else:
                swipe_center(choice(SWIPE_DIRECTIONS), SwipeSpeed.Slow, 4)
            sleep(1)
        sleep(1.5)

    def change_name(self) -> None:
        objects["avatar"].force_waitap(3)
        if objects["x_news"].waitap(1.3):
            sleep(1.5)
        objects["change_name"].force_waitap(4)
        sleep(0.9)
        objects["2-16_characters"].force_waitap(5)
        sleep(1.2)
        write(self.name)
        sleep(3)
        objects["change_name_green"].force_waitap(5)
        sleep(1.5)
        if objects["change_name_green"].exists():
            log_raise(f"Name {self.name} already taken.")
        back()
        sleep(0.8)
        print("name has been changed")

    @cached_property
    def level(self) -> int:
        objects["avatar"].force_tap()
        if not objects["account"].wait(5):
            self.close_ad()
            return self.level
        reset_screen()
        sleep(1)
        for level, obj in castle_levels.items():
            if obj.exists():
                print(f"saved {self.name} level {level}")
                self.close_ad()
                return level
        log_raise("No castle level found.")

    def bind_account(self):
        if self.account is not None:
            return
        gmail = self.google
        objects["avatar"].force_tap()
        objects["account"].force_waitap(3)
        if not objects["undo_bind"].exists():
            objects["bind"].force_waitap(3)
            if objects["gmail"].wait(40):
                objects["gmail"].force_tap_nth(gmail)
        if objects["undo_bind"].wait(50):
            account_number = get_column("google").count(gmail) - 1  # self account
            print(
                f"bind account {self.name} to {gmail} gmail. save it as account number {account_number}"
            )
            self.account = account_number
        self.close_ad()

    def kingroad_task(self) -> bool:
        self.kingroad_claim()
        if not (
            objects["kingroad"].tap()
            or objects["hand"].tap()
            or objects["kingroad_go"].exists()
        ):
            self.close_ad()
            if not (objects["kingroad"].tap() or objects["hand"].tap()):
                return False
        if not objects["kingroad_go"].wait(3):
            self.close_ad()
            return self.kingroad_task()
        task = Task.check()
        print(f"doing task {task.name}")
        match task:
            case Task.UPGRADE:
                objects["kingroad_go"].force_waitap(10)
                sleep(1)
                self.close_bella()
                if objects["hand"].waitap(3):
                    if objects['kingroad_go'].wait(1):
                        self.kingroad_task()
                else:
                    tap_center()
                sleep(1)
                if objects["upgrade"].waitap(2) or objects["hand"].tap():
                    sleep(2)
                    self._build_need()
                return True
            case Task.POWER:
                self.to_map()
                self.close_bella()
                self.heal()
                self.recruit(horses=False)
                return True
            case Task.RECRUIT:
                if randrange(5) == 4:
                    self.claim_recruits()
                    objects['kingroad'].force_waitap(20)
            case Task.GATHER:
                objects['kingroad_go'].force_waitap(20)
                sleep(2)
                self.close_bella()
                objects['book'].force_wait(20)
                sleep(2)
                if objects['hand'].waitap(2):
                    objects['map_hand'].force_waitap(5)
                    objects['map_hand'].force_waitap(3)
                    objects["check"].force_wait(10)
                    if self.last_gather_ago > 1000:
                        self.withdraw()
                    else:
                        objects["gather"].waitap(15)
                        sleep(1.5)
                        objects["gather"].waitap(4)
                        objects["set_out"].waitap(5)
                else:
                    self.get_std_mine()
                return True

            case Task.SCOUT | Task.CONQUER:
                print(f"castle {self.name}. {task.name} task have to be done manually.")
                return False

        objects["kingroad_go"].force_waitap(8)
        sleep(1.5)
        self.close_bella()
        if objects["loading"].exists():
            objects["book"].force_wait()
            sleep(2)

        while objects["hand"].waitap(1):
            if objects["heroic_evoluation_blue"].waitap(0.7):
                objects["evolve"].waitap(5)
            if objects["go_blue"].tap():
                sleep(1)
                return False
            objects["free"].tap() or objects['free_upgrade'].tap()
            if objects["kingroad_go"].tap():
                print("tapped kingroad go inside hand loop")
            sleep(1)
            reset_screen()

        while objects["map_hand"].waitap(1):
            if objects["arrow"].wait(1):
                break
        print("no more hands")
        reset_screen()

        if objects['go'].exists():
            self.kill_monster()

        elif objects["alliance_bonuses"].tap():
            self.close_ad()
            self.join_alliance()
            return True

        if objects["unlock"].tap():
            print("beast unlocked")
            sleep(20)

        elif objects["unlock_land"].tap():
            print("unlocked land")
            sleep(0.8)

        elif objects["forge"].exists():
            self.forge()

        elif objects["go_research"].tap():
            if objects["horseshoes"].waitap(2):
                sleep(0.8)
                objects["research_blue"].waitap(2)

        elif objects["research"].exists():
            if not self.speed_up():
                self.research()

        elif objects["recruit"].tap():
            print("recruiting")
            objects["recruit_blue"].wait(2)
        objects["recruit_blue"].tap()

        if objects["upgrade"].tap() or objects["upgrade_barracks"].tap():
            sleep(2)
        self._build_need()

        if objects["fortify"].tap():
            objects["one-tap_upgrade"].force_waitap(2)
            if not objects["use_all"].waitap(2):
                self.close_ad()
                self.conjure()
                return True

        if objects["sell"].tap():
            print("shop")
            sleep(1.5)
            objects["shell"].tap_each()
            objects["buy"].force_waitap(2)
            objects["shell"].wait()
            objects["shell"].tap_each()
            objects["confirm_shell"].waitap(1)
            back()

        if not objects["green"].tap() and objects["switch_level"].tap():
            for _ in range(4):
                objects["green"].force_tap_nth(randrange(15))

        if objects['no_suppress'].exists():
            back()
            sleep(1)
            objects['rebels'].force_wait(10)

        if rebels := objects["rebels"].count():
            objects['rebels'].force_tap_nth(rebels - 1)
            sleep(1.5)
            self.close_bella()
            objects["suppress"].force_wait(10)

        if objects["suppress"].tap() and not objects["set_out"].waitap(2):
            self.close_ad()
            self.to_map()
            self.withdraw()
            self.close_ad()
            return True
        else:
            objects['set_out'].tap()

        if objects["alliance_donate"].tap():
            sleep(1.5)
            objects["donate_blue"].spam_tap(4, 0.6)
            objects["donate_confirm"].waitap(3)

        elif objects["bright_challenge"].exists():
            self.challenge()
        if (
            objects["man"].exists()
            or objects["blue_bonus"].tap()
            or objects["confirm_bonus"].tap()
        ):
            self.kill_monsters()

        self.speed_up()
        self.close_ad()
        return True

    @classmethod
    def kingroad_claim(cls):
        """claims completed kingroad tasks"""
        objects["kingroad"].tap()
        if objects["kingroad_done"].waitap(2):
            print("finished kingroad chapter!")
            cls.close_ad()
            cls.kingroad_claim()
        else:
            reset_screen()
            while objects["kingroad_claim"].waitap(0.7):
                print("claimed kingroad task!")
                sleep(1.5)
                back()

    def log_into_account(self) -> None:
        """logs into current account. from city or map."""
        gmail = self.google
        account = self.account
        assert (
            gmail is not None
        ), f"called log_into_account for {self.name}, but google not set in {CASTLES_DB_PATH}"
        assert (
            account is not None
        ), f"called log_into_account for {self.name}, but account not set in {CASTLES_DB_PATH}"
        if not objects[self.name].exists():
            print(f"logging into {self.name}")

            while True:
                if objects["exit_game"].exists():
                    print("invalid token.")
                    restart_app()
                    self.load()
                self.close_ad()
                if objects["avatar"].tap():
                    objects["account"].wait(4)
                if objects["account"].tap():
                    objects["switch"].force_wait(15)
                if objects["switch"].tap():
                    sleep(1.5)
                if not (objects["login"].waitap(3) and objects["gmail"].wait(10)):
                    continue
                objects["gmail"].tap_nth(gmail)
                if not objects["acc_list"].wait(15):
                    continue
                is_green = objects["green_castle"].exists()
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
        if objects["avatar"].exists() or objects["map"].exists():
            return
        print("loading game")
        while check_castle_status() == CastleStatus.NOT_IN_CASTLE:
            reset_screen()
            if objects["man"].exists():
                return
            if objects['age'].tap():
                sleep(1)
                if objects['confirm_age'].waitap(3):
                    print("confirmed age")
            now = perf_counter()
            if now - start > 200:
                print("loading timeout. restart app.")
                restart_app()
                cls.load()
            sleep(1.5)
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
                sleep(1)
                while objects["hand"].waitap(1):
                    objects["unlock"].waitap(0.6)
                print("end hand.")
            if objects["exit_game"].exists():
                restart_app()
                cls.load()
            if objects["help"].tap():
                sleep(0.5)
            else:
                objects["continue_game"].tap()
                objects["x"].tap()
                objects["x_new"].tap()
                objects["x_news"].tap()
                objects["x_swap"].tap()
                objects["claim_daily"].tap()
                objects["claim_temple"].tap()
                objects["check_beast"].tap()
            if check_castle_status() == CastleStatus.CLOSED_AD:
                break
            for _ in range(3):
                back()
                sleep(0.2)
            sleep(0.5)
            if check_castle_status() == CastleStatus.CLOSED_AD:
                break
            elif objects["no"].waitap(3):
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

    @classmethod
    def claim_quest(cls):
        if objects["quest"].tap():
            sleep(1.5)
            while objects["daily_quest_claim"].waitap(0.4):
                back()
            while objects["claim_daily_quest"].waitap(0.4):
                back()
            sleep(2.2)
            objects["growth_quest"].tap()
            for _ in range(3):
                while objects["claim_growth_quest"].waitap(3):
                    if not objects["reward"].waitap(10):
                        back()
                        sleep(1.5)
                        back()
                if not objects["another_growth_quest"].waitap(2):
                    break
            cls.close_ad()

    @classmethod
    def claim_mail(cls) -> None:
        objects["mail"].force_tap()
        if objects["delete_mail"].waitap(3):
            objects['confirm_use_stamina'].force_waitap(10)
            sleep(2)
        for _ in range(objects["mail_reward"].count()):
            cls.close_ad()
            objects['mail'].force_tap()
            objects['mail_reward'].force_waitap(10)
            if not objects["claim_torch"].waitap(2):
                objects["read_claim_all"].force_waitap(10)
                objects["confirm_green"].force_waitap(10)
        cls.close_ad()

    @classmethod
    def claim(cls) -> None:
        """claims recruited troop and gift. from city"""
        cls.close_ad()
        if objects["claim"].tap():
            sleep(1.5)
            back()
            sleep(1.5)
        objects["help"].tap()

    @classmethod
    def events(cls) -> None:
        def event():
            if not objects["event"].exists():
                objects["events"].force_tap()
                objects["event"].force_wait(10)

        def claim_7_march(event_index: int = 0):
            event()
            if not objects["7-day_march"].tap():
                return

            sleep(0.5)
            objects["!"].wait(3)
            if objects["event_claim"].exists():
                objects["event_claim"].tap_each()
                sleep(0.5)
                back()
                back()
                cls.close_ad()
                claim_7_march(event_index + 1)
            elif objects["!"].tap_nth(event_index):
                objects["event_claim"].wait(2)
                claim_7_march(event_index + 1)
            cls.close_ad()

        def claim_rise():
            event()
            if objects["rising_road"].tap() or objects['dragons_domain'].tap():
                sleep(2)
                while objects["event_arrow"].waitap(4):
                    sleep(2)
                    back()
                cls.close_ad()

        def camel():
            event()
            if objects["camel"].tap():
                sleep(1)
                if objects["!"].waitap(2):
                    sleep(2)
                    while objects['event_claim'].waitap(2):
                        sleep(2)
                        back()
                    sleep(2)
                    if objects["!"].tap_nth(1):
                        objects['event_claim'].force_wait(10)
                        while objects['event_claim'].tap_nth(1):
                            sleep(1)
                            back()
                            sleep(2)
                cls.close_ad()

        def autumn_login():
            event()
            if objects['autumn_login'].tap():
                sleep(2)
                objects['event_claim'].tap_each()
                cls.close_ad()

        print("claiming events rewards")
        claim_7_march()
        claim_rise()
        camel()
        autumn_login()
        cls.close_ad()

    @classmethod
    def pinata(cls) -> None:
        objects['tasks'].force_tap()
        sleep(2)
        for _ in range(3):
            swipe_center(Direction.Up, SwipeSpeed.Turbo, 0.5)
            sleep(1)
        if not (objects['pinata_task'].waitap(2) and objects['pinata'].wait(3)):
            back()
            sleep(1)
            return
        for _ in range(2):
            objects['pinata'].tap_each()
            if objects['try_luck'].waitap(7):
                sleep(2)
                objects['card'].force_waitap(10)
                objects['free_crystal'].force_waitap(10)
                objects['fold'].force_waitap(10)
                objects['confirm_use_stamina'].force_waitap(10)
                objects['pinata'].wait(3)
        cls.close_ad()

    @classmethod
    def upgrade_lord_skills(cls) -> None:
        print("upgrading lord skills")
        objects["lord_info"].tap()
        if not objects["lord_skills"].waitap(10):
            cls.close_ad()
            cls.upgrade_lord_skills()
            return
        objects["development_skills"].force_waitap(10)
        sleep(0.5)
        while not objects["skill_points_0"].exists():
            if objects["upgrade_to_max"].exists():
                break
            while not objects["lord_skill"].waitap(1):
                swipe_center(Direction.Up, SwipeSpeed.Fast, 0.4)
                sleep(1.5)
            objects["upgrade_to_max"].force_waitap(3)
        cls.close_ad()

    @staticmethod
    def use_lord_skills() -> None:
        """use lord skills, harvest, gather speed up, recall all. from city or map"""
        print("lord skills...")
        objects["lord"].tap()
        if objects["gather_speed_up"].waitap(2):
            objects["use"].waitap(2)
        if objects["harvest"].waitap(2):
            objects["use"].waitap(2)
        objects["recall_all"].waitap(3)
        sleep(0.15)
        if not objects["use"].waitap(2):
            back()
            objects["use"].waitap(2)
        print("lord skills done.")
        reset_screen()
        sleep(1.2)

    def confirm_rss(self) -> bool:
        self.mine_type = chain(
            ((level, mine_type) for level, mine_type in zip(MINE_LEVELS_SEQUENCE, MineType.check_need())),
            self.mine_type,
        )
        return objects['confirm_rss'].tap()

    def heal(self) -> None:
        """heal troops in hospital and sanctuary, then claim healed. from castle."""
        if objects["claim_healed"].tap():
            print("claimed healed")
            sleep(1.5)
        if objects["hospital"].tap():
            print("healing...")
            objects["heal"].waitap(3)
            sleep(1)
            if self.confirm_rss():
                sleep(1.5)
        if objects["ask_help"].waitap(0.2):
            objects["sanctuary"].wait(2)
        if objects["sanctuary"].tap():
            print("sanctuary...")
            objects["revive"].waitap(3)
            objects["claim_holy_water"].waitap(1)
            if not objects["confirm_green"].waitap(1):
                objects["holy_quest"].waitap(1)
                objects["claim_holy_quest"].waitap(1)
                if objects["confirm_green"].waitap(1):
                    sleep(0.8)
                objects["holy_revival"].waitap(1)
            objects["revive"].waitap(1)
            sleep(0.5)
            back()
            objects["hospital_building"].wait(2)
        if objects["hospital_building"].tap():
            sleep(1.5)
        if self.speed_up():
            sleep(2)
        objects["claim_healed"].tap()

    def speed_up(self) -> bool:
        if objects["no_speed"].exists() or objects['use_speed'].exists():
            self.no_speed += 1
            return False

        if (
            objects["speed_up"].tap()
            or objects["speed_up_blue"].tap()
            or objects["get_now"].tap()
        ):
            sleep(1)
            self.no_speed += 1

        if objects["one-tap_speed_up"].tap() and objects["confirm_speed_up"].waitap(3):
            sleep(1.5)
            self.no_speed -= 1
            return True

        return False

    def research(self) -> None:
        marches = self.marches
        objects["tasks"].force_tap()
        sleep(1)
        objects["research_task"].force_waitap(10)
        if not objects["military"].wait(2):
            objects["back"].force_tap()
        objects["military"].force_wait(10)
        match marches, self.level:
            case 1, lv if lv >= 5:
                print("unlocking 2nd march")
                objects["military"].force_tap()
                if not objects["legion"].waitap(1.5):
                    if not objects["expansion"].tap():
                        objects["draft"].force_tap()
            case 2, lv if lv >= 12:
                print("unlocking 3rd march")
                objects["military"].force_tap()
                swipe_center(Direction.Up, SwipeSpeed.Normal, 1)
                if not objects["legion"].waitap(1.5):
                    if not objects["leadership"].tap():
                        objects["horseshoes"].force_tap()
            case 3, lv if lv >= 19:
                print("unlocking 4th march")
                objects["military"].force_tap()
                swipe_center(Direction.Up, SwipeSpeed.Turbo, 0.7)
                if not objects["legion"].waitap(1.5):
                    if not objects["horseshoes"].tap():
                        if not objects["expansion"].tap():
                            objects["draft"].force_tap()
            case _:
                print("researching resources technology.")
                objects["resources"].force_tap()
                sleep(3)
                for techno in sample(resources_technology, k=len(resources_technology)):
                    if techno.tap():
                        if objects["research_blue"].wait(1.5):
                            break
                        else:
                            back()
                            sleep(1)

        objects["research_blue"].waitap(1)
        self.close_ad()

    @classmethod
    def forge(cls) -> None:
        print("forging")
        if objects["forge"].tap():
            sleep(0.8)
        max_item: ScreenObject | None = None
        max_num = 0
        for item in equipment:
            item.force_tap()
            sleep(0.8)
            n = objects["forge_green"].count()
            if n >= max_num:
                max_num = n
                max_item = item
            back()
            sleep(0.8)
        if max_item is not None:
            max_item.tap()
            objects["forge_green"].wait(10)
            objects["forge_green"].tap_nth(max_num - 1)
            if objects["+"].waitap(1):
                objects["select"].waitap(3)
            objects["forge_blue"].waitap(5)
        cls.close_ad()

    def _build_need(self, *, recursive: int=0) -> bool:
        """builds required for upgrade buildings. from upgrade menu."""
        reset_screen()
        if recursive == 10:
            return self.speed_up()
        elif objects["free"].tap() or objects['free_upgrade'].tap():
            print("built for free.")
            sleep(0.5)
            self._build_need()
            return True
        if self.confirm_rss():
            return True
        elif MineType.check_need():
            print("Not enough rss even with pack.")
            self.no_speed = 1000 - 7
            return False
        if (
            objects["hand"].waitap(1)
            or objects["upgrade_blue"].tap()
            or objects["big_upgrade_blue"].tap()
            or objects["hammer_use"].tap()
            or objects["hammer_200"].tap()
            or objects["go_upgrade"].tap()
        ):
            sleep(1)
            return self._build_need(recursive=recursive+ 1)

        return self.speed_up()

    def upgrade_castle(self) -> None:
        """upgrades castle or required buildings."""
        if not objects["castle_building"].tap():
            self.to_map()
            self.close_ad()
            objects["castle_building"].force_waitap(20)
        if objects["upgrade"].waitap(2):
            sleep(2)
        self._build_need()

    def build(self) -> bool:
        self.close_ad()
        print("building")
        objects["tasks"].force_tap()
        objects["build_task"].force_waitap(10)
        sleep(1)
        objects["hand"].waitap(2)

        if objects["upgrade"].waitap(1.5):
            sleep(1.5)
        return self._build_need()

    def claim_recruits(self) -> None:
        self.close_ad()
        objects['tasks'].force_tap()
        objects['recruit_task'].force_wait(10)
        barracks = objects['recruit_task'].count()
        back()
        sleep(2)
        for i in range(barracks):
            objects['tasks'].force_waitap(10)
            if not objects['recruit_task'].wait(3):
                self.claim_recruits()
            objects['recruit_task'].force_tap_nth(i)
            sleep(2)
            if not objects['hand'].waitap(1):
                tap_center()
            if objects['speed_up'].wait(2):
                sleep(1)
                reset_screen()
                self.speed_up()
            self.close_ad()

    def recruit(self, *, horses: bool) -> None:
        """recruits horses."""
        print(f"recruiting {"horses" if horses else "powerful troops"}.")
        self.close_ad()
        objects["tasks"].force_tap()
        objects["recruit_task"].wait(1.5)
        barracks = objects["recruit_task"].count()
        back()
        sleep(2)
        for i in range(barracks * 2):
            self.close_ad()
            objects["tasks"].force_waitap(5)
            sleep(1.5)
            objects["recruit_task"].tap_nth(i % barracks)
            sleep(1)
            objects["hand"].waitap(4)
            sleep(1)
            if not objects["recruit"].waitap(3):
                objects["free"].tap()
                sleep(1)
                continue
            if not objects["recruit_blue"].wait(2):
                self.speed_up()
                continue
            if objects["x_news"].tap():
                sleep(1.5)
            if horses:
                objects["cavalry"].waitap(3)
                sleep(1.2)
                objects["previous"].spam_tap(8, 0.02)
                sleep(0.3)
                objects["second"].force_waitap(10)
                if objects['upgrade_barracks'].waitap(2):
                    sleep(1)
                    self._build_need()
                    continue
            else:
                choice(troops).waitap(3)
                sleep(0.2)
            objects['recruit_blue'].force_waitap(5)
            sleep(1)
            self.confirm_rss()
        back()
        sleep(0.5)

    @classmethod
    def conjure(cls):
        if not objects['altar'].tap():
            cls.to_map()
            cls.close_ad()
            objects['altar'].force_waitap(10)
        sleep(2)
        objects['conjure'].force_waitap(10)
        objects['conjure_10_times'].force_wait(10)
        for i in [1, 0]:
            objects['conjure_10_times'].force_tap_nth(i)
            if objects['confirm_use_stamina'].waitap(2):
                break
            back()
            reset_screen()
            sleep(1)
        cls.close_ad()

    @classmethod
    def use_pack(cls):
        """Uses items from the pack."""
        cls.close_ad()
        objects["pack"].force_tap()
        sleep(1.5)
        for i in range(objects["use_blue"].count()):
            if not objects["use_blue"].wait(1):
                cls.close_ad()
                objects["pack"].force_tap()
                objects["use_blue"].force_wait(5)
            if not objects["use_blue"].tap_nth(i):
                break
            if objects["use_all_items"].waitap(1):
                objects["use_all"].force_waitap(10)
                continue
            else:
                objects["max_items"].tap()
            objects["use_item"].waitap(1)
        cls.close_ad()

    @classmethod
    def join_alliance(cls) -> None:
        objects['alliance'].force_tap()
        if objects['alliance_bonuses'].waitap(2):
            objects['apply'].wait(2)
        if not (objects['apply'].exists() or objects['join'].exists()):
            cls.close_ad()
            return
        for _ in range(3):
            if objects['join'].tap():
                break
            objects["apply"].tap_each()
            swipe_center(Direction.Up, SwipeSpeed.Fast, 0.5)
            sleep(2)
        cls.close_ad()

    # TODO: add the remaining reward-claim flows:
    #
    # Alliance:
    #   - gifts
    #
    # Events:
    #   - add the remaining events
    #
    # City buildings:
    #   - safe resources
    #   - Castle Growth Map

    @classmethod
    def alliance_rewards(cls) -> None:
        objects['alliance'].force_tap()
        if objects['alliance_quest'].waitap(3):
            objects['claim_all'].waitap(2)
            cls.close_ad()
            objects['alliance'].force_tap()
            sleep(1)
        swipe_center(Direction.Up, SwipeSpeed.Slow, 1)
        objects['fiend_trial'].force_waitap(10)
        sleep(2)
        while objects['battle'].waitap(1):
            objects['set_out'].force_waitap(10)
            objects['skip'].force_waitap(10)
            objects['confirm_green'].force_waitap(10)
            objects['ok'].force_waitap(10)
            sleep(2)
        cls.close_ad()

    @classmethod
    def to_map(cls) -> None:
        """Goes to map from inside city"""
        cls.close_ad()
        objects["map"].force_tap()
        if not objects["book"].wait(10):
            cls.to_map()
            return
        sleep(1)
        reset_screen()

    def free_marches(self) -> int:
        """get number of available marches of current castle"""
        if check_map_status() == MapStatus.NOT_AT_MAP:
            log_raise("tried to check free marches while not at map")
        limit = self.marches
        if objects["more_marches"].tap():
            sleep(1)
        busy = objects["withdraw"].count() + objects["speed_up_march"].count()
        free = limit - busy
        print(f"available {free}/{limit} marches")
        assert 0 <= free <= limit
        return free

    @staticmethod
    def withdraw() -> bool:
        if objects["withdraw"].spam_tap(2, 1):
            objects["confirm_use_stamina"].force_waitap(5)
            return True
        return False

    def kill_monster(self) -> None:
        if not self.stamina:
            return
        self.to_map()
        if self.free_marches() == 0:
            self.close_ad()
            return
        if objects["search"].tap():
            objects["monster"].force_wait(10)
        if objects["monster"].tap():
            if randrange(5) == 2:
                objects['monster_plus'].force_waitap(10)
            objects["go"].force_wait(10)
        objects["go"].spam_tap(5, 0.2)
        sleep(1)
        if not self.withdraw() and objects["arrow"].wait(2):
            objects["arrow"].force_spam_tap(2, 0.2)
        for _ in range(30):
            if objects["quick_search"].tap():
                objects["map_hand"].force_waitap(3)
                objects["arrow"].wait(2)
                objects["arrow"].spam_tap(2, 0.5)

            elif objects['attack'].tap():
                break

            else:
                tap_center()
        else:
            self.close_ad()
            return

        objects["set_out"].waitap(2)
        if objects["use_stamina"].waitap(1):
            objects["confirm_use_stamina"].force_waitap(3)
            back()
            objects["set_out"].force_waitap(3)
            sleep(1.5)
        if check_map_status() == MapStatus.NOT_AT_MAP:
            self.stamina = False
            back()
            back()

    def get_std_mine(self) -> None:
        """Gets standard mine from the map."""

        objects["search"].force_tap()
        for _ in range(24):
            level, need_type = next(self.mine_type)
            print(f"searching mine. lv {level} {need_type.name.lower()}")
            need_type.value.force_waitap(15)
            objects["plus"].spam_tap(5, 0)
            objects["minus"].spam_tap(MAX_MINE_LEVEL - level, 0)
            objects["go"].spam_tap(4, 0.1)
            objects["gather"].wait(4)

            match check_map_status():
                case MapStatus.FOUND:
                    objects["gather"].force_tap()
                    objects["gather"].force_waitap(0.7)
                    if objects["set_out"].waitap(7):
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

        if objects["x_news"].waitap(0.5):
            sleep(0.8)

        objects["elite_mines"].force_waitap(4)
        sleep(1)
        objects["blue"].wait(3)

        if not objects["blue"].tap_nth(blue):
            back()
            sleep(1)
            return False

        if not objects["gather"].waitap(5):
            return self.get_elite_mine()

        objects["set_out"].waitap(2)
        sleep(1)

        if check_map_status() == MapStatus.NOT_AT_MAP:
            self.is_enough_troops = False
            back()
            sleep(1.5)

        return True

    def grow(self):
        if self.account is None:
            self.new_account()
        else:
            self.log_into_account()
        _ = self.level
        _ = self.marches
        for i in range(100):
            print(f"made {i} task. no_speed: {self.no_speed}")
            if i % 40 == 0:
                self.claim_mail()
                self.bind_account()
                self.claim_rss()
                self.upgrade_lord_skills()
                self.pinata()
                self.events()
                self.claim_quest()
                if randrange(10) == 1:
                    self.use_pack()
                self.join_alliance()
                self.alliance_rewards()
                while self.build():
                    pass

            if i % 10 == 1:
                self.kill_monster()
                self.close_ad()
            self.claim()
            self.heal()
            if not self.kingroad_task() or self.no_speed > 6:
                break

        self.upgrade_castle()
        self.to_map()
        if self.free_marches() != 0:
            self.get_elite_mine()
        while self.free_marches() >= 1 and self.is_enough_troops:
            self.get_std_mine()

        if not self.is_enough_troops:
            self.close_ad()
            self.recruit(horses=True)

        print("don't know what to do in this castle.")
