from time import sleep

from my_packages.data.poco_coordinates import points, STEPS, COLORS
from my_packages.image_tools import image_actions, screen_states, get_coords
from my_packages.utils import inputter
from my_packages.data.accounts import farms
from my_packages.core.adb_tools import click

lv = 6  # level of mine
witch_mine = 0
which_google = 0
which_acc = 0
which_blue_MIA = 0
which_blue_ = 0


def wait_and_click(coords: list[int]):
    sleep(0.5)
    click(coords)


def repeat_click(coords: list[int], times: int):
    for _ in range(times):
        click(coords)


def point_step(name: str,
               index: int,
               times: int,
               ) -> list[int]:

    point = list(points[name])
    print(f"points[name]: {points[name]} point: {point} name: [{name}], times: {times}")
    point[index] += STEPS[name] * times
    print(f"return point: {point}")
    return point


def close_add():
    print("Closing add...")
    while not screen_states.main_menu():
        coords = get_coords.x() or points["close"]
        click(coords)


def find_another_mine():  # to find another mine if not found
    wait_and_click(point_step("mine_type", 0, witch_mine))
    repeat_click(points["minus"], 5)
    repeat_click(points["plus"], lv - 1)
    sleep(0.5)
    repeat_click(points["go_mine"], 3)
    sleep(2)


def gather_mine():
    click(points["gather"])
    sleep(0.5)
    click(points["go"])
    sleep(0.5)
    click(points["back"])


def get_mine():  # to go to basic mine from the map
    global lv, witch_mine
    click(points["search"])
    find_another_mine()
    while True:
        if screen_states.mine_found():
            print("mine found")
            if screen_states.visible_gather():  # if mine found and point gather is invisible
                print("gather visible")
            else:  # click on mine to get it visible
                print("gather not visible")
                sleep(1)
                click(points["mine"])
                sleep(2)
            click(points["mine"])
            sleep(2)
            gather_mine()
            print("gathering mine")
            witch_mine += 1
            return
        else:  # if mine not found
            if STEPS["mine_type"] > STEPS["minimum_mine_type"]:
                print("second mine type")
                STEPS["mine_type"] += STEPS["mine"]
            else:
                print("less lv")
                STEPS["mine_type"] = 0
                lv -= 1
            find_another_mine()


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
    sleep(2)
    click(points["avatar"])
    sleep(1)
    click(points["account"])
    sleep(1)
    click(points["switch"])
    sleep(1)
    click(points["login"])
    sleep(2)
    print(f"step google, {which_google}")
    click(point_step("google", 1, google))
    sleep(3)
    print(f"step acc: {which_acc}")
    click(point_step("castle", 1, castle))
    sleep(1)
    click(points["confirm"])  # go inside
    print("end second farm")


def zeroing():
    global witch_mine
    witch_mine = 0
    # there can be zeroing lv (


def loading():
    while screen_states.loading():
        print("loading")


def lord_skills():
    print("Harvesting...")
    sleep(0.5)
    click(points["lord"])
    sleep(0.5)
    click(points["harvest"])
    sleep(0.5)
    click(points["use"])
    sleep(0.3)
    click(points["recall_all"])
    sleep(0.5)
    click(points["use"])
    print("end harvest")
    wait_and_click(points["close"])
    wait_and_click(points["close"])


def inside():
    print("running inside")  # Inside the castle
    loading()
    close_add()
    lord_skills()
    click(points["map"])
    print("finished inside")
    sleep(3)


def outside(google: int, castle: int):
    print("running outside")
    get_mine()
    get_mine()

    if not get_elite(google, castle):
        get_mine()
    get_mine()


def farm_castle(google: int, castle: int):
    inside()
    outside(google, castle)
    second_farm(google, castle)
    zeroing()


def farming():
    for google in range(inputter.farm_number(), len(farms)):
        for castle in range(farms[google]):
            print(f"farming castle {castle}")
            farm_castle(google, castle)
