# standard library
from time import sleep
from os import system

# local packages
from my_packages.data.poco_coordinates import points, STEPS, COLORS
from my_packages.image_tools import image_actions, screen_states
from my_packages.utils import inputter
from my_packages.data.accounts import farms

lv = 0   # 6 lv minus that number      # lv_minuses
witch_mine = 0
which_google = 1
which_acc = 1
castle = None

def click(cords: (int, int)):
    system(f"adb shell input tap {cords[0]} {cords[1]}")

def wait():
    sleep(0.5)
    click(points["close"])

def point_step(name: str, index):
    points[name][index] = STEPS[name]

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
    sleep(0.3)
    click(points["use"])
    print("end harvest")
    wait()
    wait()

def inside():
    print("running inside")                        # Inside the castle
    # click(point_take)  # take daily gift
    for _ in range(4):  # close ad (4 times close)
        wait()  # close ad
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
    if witch_mine < 3:
        if image_actions.check_color(points["vip"]) == COLORS["vip"]:# if I don't have free march
            wait()
            wait()
            return
    click(points["go"])
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
            if STEPS["mine_type"] < STEPS["minimum_mine_type"]:
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
        click(points["elite"])
        sleep(1)
        color = image_actions.check_color(points["elite_mine"])
        if color == COLORS["blue"]:# color of blue
            click(points["elite_mine"])
            sleep(3)# too much but should work
            if not image_actions.similar_color(image_actions.check_color(points["gather_elite"]), COLORS["gather_elite"], 10):# if elite isn't occupied by another alliance
                click(points["gather_elite"])
                sleep(1)
                color = image_actions.check_color(points["vip"])
                if color != COLORS["vip"]:# if I don't need VIP # I think this color isn't True
                     if color == COLORS["occupied"]:# if somebody is going to elite mine
                         click(points["vip"])
                     click(points["go"])# regularly I should be there
                     if second_blue:
                         point_step("elite_blue", 1)
                     return True# everything is alright I went to elite
                else:
                    wait()
                    wait()
                    click(points["back"])
                    return True# if I need VIP
            else:# if elite is occupied by someone
                print("someone else is already elite")
                if second_blue:
                    point_step("elite_blue", 1)# again while
                else:
                    return False
        else:
            print("some chemistry error", color)
            click(points["favourites_back"])
            return False# if there is no elites

def second_farm():
    global which_google, which_acc
    print("running second_farm")
    if which_acc < farms[which_google]:
        point_step("castle", 1)
    else:
        which_google += 1
        point_step("google", 1)
        which_acc = 1

    sleep(2)
    click(points["avatar"])
    sleep(1)
    click(points["account"])
    sleep(1)
    click(points["switch"])
    sleep(1)
    click(points["login"])
    sleep(2)
    click(points["google"])
    sleep(3)
    click(points["castle"])
    sleep(1)
    click(points["confirm"])# go inside
    print("end second farm")
    sleep(20)# I can make the still checking there

def zeroing():
    global witch_mine
    witch_mine = 0
    # there can be zeroing lv (

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
    sleep(5)
    for _ in range(7):
        farm_castle()
        castle += 1