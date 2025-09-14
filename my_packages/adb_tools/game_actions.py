# standard library
from time import sleep
from os import system

# local packages
from my_packages.data.poco_coordinates import points, STEPS, COLORS
from my_packages.image_tools import image_actions, screen_states
from my_packages.utils import inputter
from my_packages.data.accounts import farms
from my_packages.adb_tools.adb_config import get_device_name

lv = 0   # 6 lv minus that number      # lv_minuses
witch_mine = 0
which_google = 0
which_acc = 0
castle = None
device = get_device_name()

def click(cords: (int, int)):
    system(f"adb -s {device} shell input tap {cords[0]} {cords[1]}")

def wait():
    sleep(0.5)
    click(points["close"])

def point_step(name: str, index):
    point = points[name]
    point[index] += STEPS[name]
    return point

def close_add():
    print("Closing...")
    while not screen_states.main_menu():
        if (coords := screen_states.get_coords_add()) is not None:
            click(coords)
        else:
            wait()
        sleep(0.5)

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
    wait()
    wait()

def inside():
    print("running inside")                        # Inside the castle
    # click(point_take)  # take daily gift
    close_add()
    lord_skills()
    click(points["map"])
    print("running outside")
    sleep(3)

def find_another():# to find another mine if not found
    click((points["iron"][0] + STEPS["mine_type"], points["iron"][1]))
    sleep(0.5)
    for _ in range(5):
        click(points["plus"])
    for _ in range(lv):
        click(points["minus"])
        sleep(0.5)
    for _ in range(3):
        click(points["go_mine"])
    sleep(2)

def gather_mine():
    click(points["gather"])
    sleep(0.5)
    # if witch_mine < 3:
    #     if image_actions.check_color(points["vip"]) == COLORS["vip"]:# if I don't have free march
    #         wait()
    #         wait()
    #         return
    click(points["go"])
    sleep(0.5)
    click(points["back"])

def get_mine(): # to go to basic mine from the map
    global lv, witch_mine
    click(points["search"])
    sleep(1)
    find_another()
    while True:
        if screen_states.mine_found():
            print("mine found")
            if screen_states.visible_gather():# if mine found and point gather is invisible
                print("gather visible")
            else:# click on mine to get it visible
                print("gather not visible")
                click(points["mine"])
                sleep(1)
            click(points["mine"])
            sleep(2)
            gather_mine()
            print("gathering mine")
            witch_mine += 1
            return
        else:             # if mine not found
            if STEPS["mine_type"] > STEPS["minimum_mine_type"]:
                print("second mine type")
                STEPS["mine_type"] += STEPS["mine"]
            else:
                print("less lv")
                STEPS["mine_type"] = 0
                lv += 1
            find_another()


def get_elite():
    print("Elite")
    match castle:
        case 0 | 4:
            points["elite_mine"] = points["elite_mine1"]
            second_blue = False
        case _:
            points["elite_mine"] = points["elite_blue"]
            second_blue = True
        
    while True:
        click(points["favorites"])
        sleep(1)
        click(points["alliance_elite"])
        sleep(1)
        color = image_actions.check_color(points["elite_blue"])
        if color == COLORS["elite_blue"]:# color of blue
            click(points["elite_blue"])
            sleep(3)# too much but should work
            click(points["gather_elite"])
            sleep(1)
            click(points["go"])# regularly I should be there

            if second_blue:
                points["elite_blue"] = point_step("elite_blue", 1)
            return True# everything is alright I went to elite
        else:
            print("some chemistry error", color)
            click(points["favourites_back"])
            return False# if there is no elites

def second_farm():
    global which_google, which_acc
    print("running second_farm")

    set_which(1)

    sleep(2)
    click(points["avatar"])
    sleep(1)
    click(points["account"])
    sleep(1)
    click(points["switch"])
    sleep(1)
    click(points["login"])
    sleep(2)
    click(point_step("google", 1))
    sleep(3)
    click(point_step("castle", 1))
    sleep(1)
    click(points["confirm"])# go inside
    print("end second farm")
    sleep(20)# I can make the still checking there

def zeroing():
    global witch_mine
    witch_mine = 0
    # there can be zeroing lv (

def set_which(acc_steps):
    global which_google, which_acc
    for _ in range(acc_steps):
        if which_acc < farms[which_google]:
            which_acc += 1
        else:
            which_google += 1
            which_acc = 1

def outside():
    get_mine()
    get_mine()

    if not get_elite():
        get_mine()
    get_mine()

def farm_castle():
    inside()
    outside()
    second_farm()
    zeroing()


def farming():
    global castle
    castle = inputter.farm_number()
    set_which(castle)
    for _ in range(7):
        print(f"farming castle {castle}")
        farm_castle()
        castle += 1