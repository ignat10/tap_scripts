from my_packages.utils.farm_utils import *


class Farm:
    def __init__(self, number: int, name: str, google: int, account: int, lv: int, alliance: str):
        self.number = number
        self.name = name
        self.google = google
        self.account = account
        self.lv = lv
        self.alliance = alliance
        self.mine_lv = 6
        self.mine_type = 0
        self.blue = 0

    def outside(self):
        sleep(3)
        print("running outside")
        for mine in range(4):
            if mine == 2:
                if self.get_elite():
                    continue
            self.get_mine()

    def get_mine(self):  # to go to basic mine from the map
        click(points["search"])
        while True:
            self.find_another_mine()
            match screen_states.search_state():
                case screen_states.Mine.FOUND_VISIBLE:
                    print("gather is visible")
                    break
                case screen_states.Mine.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                    print("gather is invisible")
                    click(points["gather"])
                    break
                case screen_states.Mine.NOT_FOUND:  # if mine not found
                    if self.mine_type < 4:
                        print("second mine type")
                        self.mine_type += 1
                    else:
                        print("less lv")
                        self.mine_lv -= 1
                        self.mine_type = 0
                case screen_states.Mine.NOT_MAP:
                    print("somehow I'm not at the map.\npanic")
        wait_and_click(points["mine"])
        sleep(2)
        gather_mine()

    def find_another_mine(self):  # to find another mine if not found
        wait_and_click(point_step("mine_type", 0, self.mine_type))
        repeat_click(points["minus"], 5)
        repeat_click(points["plus"], self.mine_lv - 1)
        repeat_click(points["go_mine"], 3)

    def get_elite(self):
        print("Elite")
        match self.number:
            case 0 | 0:
                which_blue = self.blue
                second_blue = False
            case _:
                which_blue = 0
                second_blue = True
        while True:
            click(points["favorites"])
            sleep(1)
            click(points["alliance_elite"])
            sleep(1)
            if screen_states.is_blue(point_step("blue", 1, 1)):  # color of blue
                click(point_step("elite_blue", 1, which_blue))
                sleep(3)  # too much but should work
                click(points["gather_elite"])
                sleep(1)
                click(points["go"])  # regularly I should be there
                if second_blue:
                    which_blue += 1
                return True  # everything is alright I went to elite
            else:
                print("some chemistry error")
                click(points["favourites_back"])
                return False  # if there is no elites

    def second_farm(self):
        print("running second_farm")
        wait_and_click(points["avatar"])
        wait_and_click(points["account"])
        wait_and_click(points["switch"])
        wait_and_click(points["login"], 1)
        print(f"step google, {self.google}")
        wait_and_click(point_step("google", 1, self.google), 2)
        print(f"step acc: {self.account}")
        wait_and_click(point_step("castle", 1, self.account), 3)
        wait_and_click(points["confirm"], 1)  # go inside
        print("end second farm")


    def farm_castle(self):
        inside()
        self.outside()
        self.second_farm()


# how to fix most likely due to a circular import

# where to storage castles

#different between self.fn || farm.fn

# gow to minimalize connection between modules and max them kol-vo

# fix get_elite excludes

# where to put general fns
