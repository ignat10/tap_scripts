from time import sleep

from my_packages.adb_tools.adb_device import device
from my_packages.data.poco_coordinates import points, STEPS
from my_packages.image_tools.screen_states import screen_state


def wait_and_click(coords: tuple[int, int], delay=0.5):
    sleep(delay)
    device.click(coords)


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


    @staticmethod
    def repeat_click(coords: tuple[int, int], times: int):
        for _ in range(times):
            device.click(coords)

    @staticmethod
    def point_step(name: str,
                   index: int,
                   times: int,
                   ) -> tuple[int, int]:
        original = tuple(points[name])
        point = list(original)
        step = STEPS[name]
        print(f"point: {point}, index: {index} step: {step}, times: {times}, name: [{name}]")
        point[index] += step * times
        print(f"return point: {point}")
        assert original != point, f"point after step hasn't been changed: {point}"
        return tuple[int, int](point)

    @staticmethod
    def close_ad():
        print("Closing ad...")
        while not  screen_state.main_menu():
            coords = screen_state.get_coords.x() or points["close"]
            device.click(coords)
            print(f"x find: {not coords == points["close"]}, {coords} pressed")
            sleep(1)
        print("Ad closed.")

    @staticmethod
    def gather_mine():
        wait_and_click(points["gather"])
        wait_and_click(points["go"])
        wait_and_click(points["back"])

    @staticmethod
    def loading():
        sleep(1)
        while  screen_state.loading():
            print("loading")
        print("loaded")

    @staticmethod
    def lord_skills():
        print("Harvesting...")
        wait_and_click(points["lord"])
        wait_and_click(points["harvest"])
        wait_and_click(points["use"])
        print("end harvest")
        wait_and_click(points["recall_all"])
        wait_and_click(points["use"])
        print("end recall_all")
        wait_and_click(points["close"])
        wait_and_click(points["close"])

    def inside(self):
        self.loading()
        print("running inside")  # Inside the castle
        self.close_ad()
        self.lord_skills()
        device.click(points["map"])
        print("finished inside")
        

    def outside(self):
        sleep(3)
        print("running outside")
        for mine in range(4):
            if mine == 2:
                if self.get_elite():
                    continue
            self.get_mine()

    def get_mine(self):  # to go to basic mine from the map
        device.click(points["search"])
        while True:
            self.find_another_mine()
            sleep(2)
            match  screen_state.search_state():
                case  screen_state.Mine.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case  screen_state.Mine.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    device.click(points["gather"])
                    break
                case  screen_state.Mine.NOT_FOUND:  # if mine not found
                    if self.mine_type < 4:
                        print("second mine type")
                        self.mine_type += 1
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = 0
                case  screen_state.Mine.NOT_MAP:
                    print("somehow I'm not at the map.\npanic")
        wait_and_click(points["mine"])
        sleep(2)
        self.gather_mine()

    def find_another_mine(self):  # to find another mine if not found
        wait_and_click(self.point_step("mine_type", 0, self.mine_type))
        self.repeat_click(points["minus"], 5)
        self.repeat_click(points["plus"], self.mine_lv - 1)
        self.repeat_click(points["go_mine"], 3)

    def get_elite(self):
        print("Elite")
        which_blue = self.blue
        while True:
            device.click(points["favorites"])
            sleep(1)
            device.click(points["alliance_elite"])
            sleep(1)
            if  screen_state.is_blue(self.point_step("elite_blue", 1, 1)):  # color of blue
                device.click(self.point_step("elite_blue", 1, which_blue))
                sleep(3)  # too much but should work
                device.click(points["gather_elite"])
                sleep(1)
                device.click(points["go"])  # regularly I should be there
                which_blue += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                device.click(points["favourites_back"])
                return False  # if there is no elites


    def switch_farm(self):
        print(f"running second_farm {self.name}")
        wait_and_click(points["avatar"])
        wait_and_click(points["account"])
        wait_and_click(points["switch"])
        wait_and_click(points["login"], 1)
        print(f"step google, {self.google}")
        wait_and_click(self.point_step("google", 1, self.google), 2)
        print(f"step acc: {self.account}")
        wait_and_click(self.point_step("castle", 1, self.account), 3)
        wait_and_click(points["confirm"], 1)  # go inside
        print(f"logged in to {self.name}")


# fix get_elite excludes

""""
8. Предлагаемый по-шаговый план работы (практический, 9 шагов)

Добавить logging и заменить print на logger. (малый)

Настроить flake8/ruff/black и pre-commit. (малый)

Добавить базовые unit-tests и workflow CI. (средний)
"""