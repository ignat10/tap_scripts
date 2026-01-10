from time import sleep
from typing import Self


from . import objects
from . import status



class Farm:
    alliances_elite_mines: dict[Self, int] = {}

    def __init__(self, name: str, lv: int, google: int, account: int, alliance: str):
        self.name = name
        self.google = google
        self.account = account
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type = 0

    @staticmethod
    def lord_skills():
        print("lord skills...")
        objects.LORD.click()
        objects.HARVEST.click(delay=0.5)
        objects.USE.click(delay=0.5)
        print("harvested. recalling...")
        objects.RECALL_ALL.click()
        objects.USE.click(delay=0.5)
        objects.CLOSE.click()
        objects.CLOSE.click()
        print("lord skills done.")

    def get_std_mine(self):  # to go to basic mine from the map

        def find_another_mine() -> None:  # to find another mine if not found
            objects.MINE_TYPE.click(repeat=self.mine_type)
            objects.MINUS.click(repeat=5)
            objects.PLUS.click(repeat=self.mine_lv - 1)
            objects.GO_MINE.click(repeat=3)

        def gather_std_mine() -> None:
            objects.GATHER.click(delay=0.5)
            objects.GO.click(delay=0.5)
            objects.BACK.click(delay=0.5)

        objects.SEARCH.click(delay=1)
        while True:
            find_another_mine()
            sleep(2)
            match status.check_status():
                case status.Status.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case status.Status.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    objects.GATHER.click()
                    break
                case status.Status.NOT_FOUND:
                    if self.mine_type < 4:
                        print("second mine type")
                        self.mine_type += 1
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = 0
                case status.Status.NOT_MAP:
                    print("somehow I'm not at the map.\npanic")
                    continue
        objects.MINE.click(delay=0.5)
        sleep(2)
        gather_std_mine()

    def get_elite_mine(self):
        print("Elite")
        while True:
            objects.BOOK.click()
            objects.ALLIANCE_ELITE_MINES.click(delay=0.5)
            sleep(1)
            if objects.BLUE.compare_part():  # color of blue
                objects.BLUE.click(steps=self.alliances_elite_mines[self])
                objects.GATHER_ELITE_MINE.click(delay=3)
                objects.GO.click(delay=1)  # regularly I should be there
                self.alliances_elite_mines[self] += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                objects.FAVORITES_BACK.click()
                return False  # if there is no elites

    def is_current_castle(self) -> bool:
        print(f"checking is current castle: {self.name}")
        return bool(getattr(objects, self.name.upper()).compare_part()) # replace with compare_part

    def second_farm(self):
        print(f"running second_farm {self.name}, google: {self.google}, account: {self.account}")
        objects.AVATAR.click(delay=0.5)
        objects.ACCOUNT.click(delay=0.5)
        objects.SWITCH.click(delay=1)
        objects.LOGIN.click(delay=1)
        objects.GOOGLE(times=self.google).click(delay=2)
        objects.CASTLE(times=self.account).click(delay=3)
        objects.CONFIRM.click(delay=1)  # go inside
        print(f"logged into {self.name}")

    def load(self):
        sleep(1)
        while objects.LOAD.compare_part():
            print(f"loading {self.name}")
        print("loaded.")

    @classmethod
    def to_map(cls):
        print("Going to the map...")
        objects.MAP.click(repeat=5)
        sleep(2)
        while not objects.BOOK.compare_part():
            (objects.XS.find_and_click() or objects.MAP).click()
            sleep(1)
        cls.lord_skills()

    def mining(self):
        print("mining...")
        for mine in range(4):
            if mine == 2:
                if self.get_elite_mine():
                    continue
            self.get_std_mine()

    def switch_farm(self):
        if self.is_current_castle():
            print(f"already {self.name}")
        else:
            self.second_farm()
            self.load()

""""TODO:
Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)
"""