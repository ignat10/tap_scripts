from time import sleep

from my_packages.adb_tools.device_actions import click
from my_packages.data.poco_coordinates import Points
from my_packages.image_tools import image_analyzer
from my_packages.image_tools.image_manager import Folders


def wait_and_click(coords: tuple[int, int], delay=0.5):
    sleep(delay)
    click(coords)


def repeat_click(coords: tuple[int, int], times: int):
    for _ in range(times):
        click(coords)


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

    def is_current_castle(self) -> bool:
        return bool(image_analyzer.find_part(self.name))

    def load(self):
        sleep(1)
        while image_analyzer.compare_screen(Folders.LOAD):
            print(f"loading {self.name}")
        print("loaded.")

    @staticmethod
    def to_map():
        print("Going to the map...")
        repeat_click(Points.map, 5)
        while not image_analyzer.find_part(Folders.CITIES):
            coords = image_analyzer.find_part(Folders.XS) or Points.map
            click(coords)
            print(f"x find: {coords != Points.close}, {coords} pressed")
            sleep(1)
        print("at the map. lord skills...")
        Farm.lord_skills()
        print("lord skills done.")


    @staticmethod
    def lord_skills():
        print("Harvesting...")
        wait_and_click(Points.lord)
        wait_and_click(Points.harvest)
        wait_and_click(Points.use)
        print("harvested. recalling...")
        wait_and_click(Points.recall_all)
        wait_and_click(Points.use)
        print("end recall_all")
        wait_and_click(Points.close)
        wait_and_click(Points.close)

    def find_another_mine(self):  # to find another mine if not found
        wait_and_click(Points.mine_type(index=0, times=self.mine_type))
        repeat_click(Points.minus, 5)
        repeat_click(Points.plus, self.mine_lv - 1)
        repeat_click(Points.go_mine, 3)

    @staticmethod
    def gather_mine():
        wait_and_click(Points.gather)
        wait_and_click(Points.go)
        wait_and_click(Points.back)
        
    def get_mine(self):  # to go to basic mine from the map
        click(Points.search)
        while True:
            self.find_another_mine()
            sleep(2)
            match  image_analyzer.check_status():
                case  image_analyzer.Status.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case  image_analyzer.Status.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    click(Points.gather)
                    break
                case  image_analyzer.Status.NOT_FOUND:
                    if self.mine_type < 4:
                        print("second mine type")
                        self.mine_type += 1
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = 0
                case  image_analyzer.Status.NOT_MAP:
                    print("somehow I'm not at the map.\npanic")
        wait_and_click(Points.mine)
        sleep(2)
        self.gather_mine()

    def get_elite(self):
        print("Elite")
        which_blue = self.blue
        while True:
            click(Points.favorites)
            sleep(1)
            click(Points.alliance_elite)
            sleep(1)
            if image_analyzer.compare_part(Points.elite_blue(index=1, times=self.blue)):  # color of blue
                click(Points.elite_blue(index=1, times=which_blue))
                sleep(3)  # too much but should work
                click(Points.gather_elite)
                sleep(1)
                click(Points.go)  # regularly I should be there
                which_blue += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                click(Points.favorites_back)
                return False  # if there is no elites

    def mining(self):
        print("mining...")
        for mine in range(4):
            if mine == 2:
                if self.get_elite():
                    continue
            self.get_mine()
            
    def second_farm(self):
        print(f"running second_farm {self.name}")
        wait_and_click(Points.avatar)
        wait_and_click(Points.account)
        wait_and_click(Points.switch)
        wait_and_click(Points.login, 1)
        print(f"google account, {self.google}")
        wait_and_click(Points.google(index=1, times=self.google), 2)
        print(f"castle account: {self.account}")
        wait_and_click(Points.castle(index=1, times=self.account), 3)
        wait_and_click(Points.confirm, 1)  # go inside
        print(f"logged in to {self.name}")

    def switch_farm(self):
        if self.is_current_castle():
            print(f"already {self.name}")
        else:
            self.second_farm()


def make_castles() -> list[Farm]:
    from my_packages.data.farms import farms_sheet
    from my_packages.utils.inputter import farm_number

    return [Farm(*row) for row in farms_sheet.values[farm_number(0)::]]


# fix get_elite excludes

""""
8. Предлагаемый по-шаговый план работы (практический, 9 шагов)

Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)

Добавить базовые unit-tests и workflow CI. (средний)
"""