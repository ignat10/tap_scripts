from time import sleep

from my_packages.adb_tools.device_actions import click
from my_packages.data.poco_coordinates import Point, PointData
from my_packages.image_tools import screen_states


def wait_and_click(coords: tuple[int, int], delay=0.5):
    sleep(delay)
    click(coords)


def repeat_click(coords: tuple[int, int], times: int):
    for _ in range(times):
        click(coords)


def point_step(point: PointData,
               index: int,
               times: int,
               ) -> tuple[int, int]:
    original = tuple(point)
    step = float(point.gap) if point.gap is not None else exit("There's no step!")
    point = list(original)
    print(f"(point: {point}, index: {index}) (step: {step}, times: {times})")
    point[index] += step * times
    print(f"return point: {point}")
    return tuple(point)


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
        return bool(screen_states.is_avatar(self.name))

    def loading(self):
        sleep(1)
        while  screen_states.loading():
            print(f"loading {self.name}")
        print("loaded")

    @staticmethod
    def close_ad():
        print("Closing ad...")
        repeat_click(Point.map, 5)
        while not  screen_states.map() or screen_states.main_menu():
            coords = screen_states.get_coords() or Point.close
            click(coords)
            print(f"x find: {not coords == Point.close}, {coords} pressed")
            sleep(1)
        print("Ad closed.")

    @staticmethod
    def lord_skills():
        print("Harvesting...")
        wait_and_click(Point.lord)
        wait_and_click(Point.harvest)
        wait_and_click(Point.use)
        print("end harvest")
        wait_and_click(Point.recall_all)
        wait_and_click(Point.use)
        print("end recall_all")
        wait_and_click(Point.close)
        wait_and_click(Point.close)

    def inside(self):
        self.loading()
        print("running inside")  # Inside the castle
        self.close_ad()
        self.lord_skills()
        click(Point.map)
        print("finished inside")

    def find_another_mine(self):  # to find another mine if not found
        wait_and_click(point_step("mine_type", 0, self.mine_type))
        repeat_click(Point.minus, 5)
        repeat_click(Point.plus, self.mine_lv - 1)
        repeat_click(Point.go_mine, 3)

    @staticmethod
    def gather_mine():
        wait_and_click(Point.gather)
        wait_and_click(Point.go)
        wait_and_click(Point.back)
        
    def get_mine(self):  # to go to basic mine from the map
        click(Point.search)
        while True:
            self.find_another_mine()
            sleep(2)
            match  screen_states.check_status():
                case  screen_states.Status.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case  screen_states.Status.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    click(Point.gather)
                    break
                case  screen_states.Status.NOT_FOUND:
                    if self.mine_type < 4:
                        print("second mine type")
                        self.mine_type += 1
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = 0
                case  screen_states.Status.NOT_MAP:
                    print("somehow I'm not at the map.\npanic")
        wait_and_click(Point.mine)
        sleep(2)
        self.gather_mine()

    def get_elite(self):
        print("Elite")
        which_blue = self.blue
        while True:
            click(Point.favorites)
            sleep(1)
            click(Point.alliance_elite)
            sleep(1)
            if screen_states.is_blue(point_step("elite_blue", 1, self.blue)):  # color of blue
                click(point_step("elite_blue", 1, which_blue))
                sleep(3)  # too much but should work
                click(Point.gather_elite)
                sleep(1)
                click(Point.go)  # regularly I should be there
                which_blue += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                click(Point.favourites_back)
                return False  # if there is no elites

    def outside(self):
        sleep(3)
        print("running outside")
        for mine in range(4):
            if mine == 2:
                if self.get_elite():
                    continue
            self.get_mine()
            
    def second_farm(self):
        print(f"running second_farm {self.name}")
        wait_and_click(Point.avatar)
        wait_and_click(Point.account)
        wait_and_click(Point.switch)
        wait_and_click(Point.login, 1)
        print(f"step google, {self.google}")
        wait_and_click(point_step("google", 1, self.google), 2)
        print(f"step acc: {self.account}")
        wait_and_click(point_step("castle", 1, self.account), 3)
        wait_and_click(Point.confirm, 1)  # go inside
        print(f"logged in to {self.name}")

    def switch_farm(self):
        if not self.is_current_castle():
            self.second_farm()
        else:
            print(f"already {self.name}")

# fix get_elite excludes

""""
8. Предлагаемый по-шаговый план работы (практический, 9 шагов)

Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)

Добавить базовые unit-tests и workflow CI. (средний)
"""