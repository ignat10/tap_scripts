from time import sleep


from ..data import points
from ..image_tools import templates
from . import status



class Farm:
    def __init__(self, name: str, lv: int, google: int, account: int, alliance: str):
        self.name = name
        self.google = google
        self.account = account
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type = 0
        self.blue = 0


    def find_another_mine(self):  # to find another mine if not found
        points.MINE_TYPE(index=0, times=self.mine_type).click()
        points.MINUS.repeat_click(5)
        points.PLUS.repeat_click(self.mine_lv - 1)
        points.GO_MINE.repeat_click(3)

    @staticmethod
    def gather_mine():
        points.GATHER.wait_and_click()
        points.GO.wait_and_click()
        points.BACK.wait_and_click()

    @staticmethod
    def lord_skills():
        print("Harvesting...")
        points.LORD.wait_and_click()
        points.HARVEST.wait_and_click()
        points.USE.wait_and_click()
        print("harvested. recalling...")
        points.RECALL_ALL.wait_and_click()
        points.USE.wait_and_click()
        points.CLOSE.click()
        points.CLOSE.click()
        print("skilled.")

    def get_mine(self):  # to go to basic mine from the map
        points.SEARCH.click()
        while True:
            self.find_another_mine()
            sleep(2)
            match status.check_status():
                case status.Status.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case status.Status.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    points.GATHER.click()
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
        points.MINE.wait_and_click()
        sleep(2)
        self.gather_mine()

    def get_elite(self):
        print("Elite")
        which_blue = self.blue
        while True:
            points.FAVORITES.click()
            points.ALLIANCE_ELITE.wait_and_click()
            sleep(1)
            templates.BLUE.coords = points.elite_blue(index=1, times=self.blue)
            if templates.BLUE.compare_part():  # color of blue
                points.ELITE_BLUE(index=1, times=which_blue).click()
                points.GATHER_ELITE.wait_and_click(3)
                points.GO.wait_and_click(1)  # regularly I should be there
                which_blue += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                points.FAVORITES_BACK.click()
                return False  # if there is no elites

    def is_current_castle(self) -> bool:
        print(f"checking is current castle: {self.name}")
        return bool(getattr(templates, self.name.upper()).find_part())

    def second_farm(self):
        print(f"running second_farm {self.name}, google: {self.google}, account: {self.account}")
        points.AVATAR.wait_and_click()
        points.ACCOUNT.wait_and_click()
        points.SWITCH.wait_and_click(1)
        points.LOGIN.wait_and_click(1)
        points.GOOGLE(index=1, times=self.google).wait_and_click(2)
        points.CASTLE(index=1, times=self.account).wait_and_click(3)
        points.CONFIRM.wait_and_click(1)  # go inside
        print(f"logged into {self.name}")

    def load(self):
        sleep(1)
        while templates.LOAD.compare_full():
            print(f"loading {self.name}")
        print("loaded.")

    @classmethod
    def to_map(cls):
        print("Going to the map...")
        points.MAP.repeat_click(5)
        sleep(2)
        while not templates.CITIES.find_part():
            coords = templates.XS.find_part() or points.MAP
            coords.click()
            print(f"x find: {coords != points.CLOSE}, {coords} pressed")
            sleep(1)
        print("at the map. lord skills...")
        cls.lord_skills()
        print("lord skills done.")

    def mining(self):
        print("mining...")
        for mine in range(4):
            if mine == 2:
                if self.get_elite():
                    continue
            self.get_mine()

    def switch_farm(self):
        if self.is_current_castle():
            print(f"already {self.name}")
        else:
            self.second_farm()
            self.load()


# fix get_elite excludes

""""TODO:
Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)
"""