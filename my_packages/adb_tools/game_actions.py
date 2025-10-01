from time import sleep

from my_packages.data.poco_coordinates import points, STEPS, COLORS
from my_packages.data import farms
from my_packages.image_tools import image_actions, screen_states, get_coords
from my_packages.utils import inputter
from my_packages.core.adb_tools import click

which_blue_MIA = 0
which_blue_ = 0


def wait_and_click(coords: tuple[int, int], delay=0.5):
    sleep(delay)
    click(coords)


def repeat_click(coords: tuple[int, int], times: int):
    for _ in range(times):
        click(coords)


def point_step(name: str,
               index: int,
               times: int,
               ) -> tuple[int, int]:

    point = points[name]
    step = STEPS[name]
    print(f"point: {point}, index: {index} step: {step}, times: {times}, name: [{name}]")
    point[index] += step * times
    print(f"return point: {point}")
    assert points[index] != point, f"point after step hasn't been changed: {point}"
    return point


def close_add():
    print("Closing add...")
    while not screen_states.main_menu():
        coords = get_coords.x() or points["close"]
        click(coords)


def find_another_mine(lv, mine_type):  # to find another mine if not found
    wait_and_click(point_step("mine_type", 0, mine_type))
    repeat_click(points["minus"], 5)
    repeat_click(points["plus"], lv - 1)
    repeat_click(points["go_mine"], 3)


def gather_mine():
    wait_and_click(points["gather"])
    wait_and_click(points["go"])
    wait_and_click(points["back"])


def get_mine(lv: int, mine_type: int):  # to go to basic mine from the map
    click(points["search"])
    while True:
        find_another_mine(lv, mine_type)
        match screen_states.search_state():
            case screen_states.Mine.FOUND_VISIBLE:
                print("gather is visible")
                break
            case screen_states.Mine.FOUND_NOT_VISIBLE:  # if mine found but point gather is invisible
                print("gather is invisible")
                click(points["mine"])
                break
            case screen_states.Mine.NOT_FOUND: # if mine not found
                if mine_type < 4:
                    print("second mine type")
                    mine_type += 1
                else:
                    print("less lv")
                    lv -= 1
                    mine_type = 0
            case screen_states.Mine.NOT_MAP:
                print("somehow I'm not at the map.\npanic")
    wait_and_click(points["mine"])
    sleep(2)
    gather_mine()
    return lv, mine_type


def get_elite(google: int, castle: int):
    print("Elite")
    match (google, castle):
        case (0, 0) | (2, 1):
            which_blue = 0
            second_blue = False
        case _:
            which_blue = which_blue_MIA
            second_blue = True
    while True:
        click(points["favorites"])
        sleep(1)
        click(points["alliance_elite"])
        sleep(1)
        color = image_actions.check_color(points["elite_blue"])
        if color == COLORS["elite_blue"]:  # color of blue
            click(point_step("elite_blue", 1, which_blue))
            sleep(3)  # too much but should work
            click(points["gather_elite"])
            sleep(1)
            click(points["go"])  # regularly I should be there
            if second_blue:
                which_blue += 1
            return True  # everything is alright I went to elite
        else:
            print("some chemistry error", color)
            click(points["favourites_back"])
            return False  # if there is no elites


def second_farm(google: int, castle: int):
    print("running second_farm")
    wait_and_click(points["avatar"])
    wait_and_click(points["account"])
    wait_and_click(points["switch"])
    wait_and_click(points["login"], 1)
    print(f"step google, {google}")
    wait_and_click(point_step("google", 1, google), 2)
    print(f"step acc: {castle}")
    wait_and_click(point_step("castle", 1, castle), 3)
    wait_and_click(points["confirm"], 1)  # go inside
    print("end second farm")


def loading():
    while screen_states.loading():
        print("loading")
    print("loaded")


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


def inside():
    loading()
    print("running inside")  # Inside the castle
    close_add()
    lord_skills()
    click(points["map"])
    print("finished inside")


def outside(google: int, castle: int):
    sleep(3)
    print("running outside")
    lv = 6  # level of mine
    mine_type = 0
    for mine in range(4):
        if mine == 2:
            if get_elite(google, castle):
                continue
        lv, mine_type = get_mine(lv, mine_type)


def farm_castle(google: int, castle: int):
    inside()
    outside(google, castle)
    second_farm(google, castle)


def farming():
    for google in range(inputter.farm_number(), len(farms)):
        print(f"google: {google}")
        for castle in range(farms[google]):
            print(f"farming castle {castle}")
            farm_castle(google, castle)
