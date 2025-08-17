# standard library
from time import sleep
from os import system
from subprocess import run

from PIL import Image

from my_packages import points, steps, colors

lv = 0 # iron first than - that
mine_type = 0 # 6 lv minus that number
witch_mine = 0
acc: bool = True

def click(cords: (int, int)):
    system(f"adb shell input tap {cords[0]} {cords[1]}")

def wait():
    sleep(0.5)
    click(points["close"])

def make_screen():
    with open(f"screen.png", "wb") as f:
        run(["adb", "exec-out", "screencap", "-p"], stdout = f)
    return Image.open("screen.png")

def get_pixel(screen, cords):
    return screen.getpixel(cords)

def check_color(point_checking: (int, int)):
    return make_screen().getpixel((point_checking[0], point_checking[1]))

def similar_color(color: (int, int, int, int), another_color: (int, int, int, int), tolerance: int) -> bool:
    return all(abs(a - t < tolerance) for a, t in zip(another_color, color))

def lord_skills():
    print("Harvesting...")
    sleep(0.5)
    click(points["lord"])
    sleep(0.5)
    click(points["harvest"])
    sleep(0.5)
    click(points["use"])
    sleep(0.5)
    wait()
    click(points["recall_all"])
    sleep(0.5)
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
    global mine_type, lv
    click((points["iron"][0] - mine_type, points["iron"][1]))
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
        if check_color(points["vip"]) == (0, 132, 162, 255):# if I don't have free march
            wait()
            wait()
            return
    click(points["go"])
    click(points["back"])

def get_mine(): # to go to basic mine from the map
    global mine_type, lv, witch_mine
    click(points["search"])
    sleep(1)
    find_another()
    while True:
        img = make_screen()
        if similar_color(colors["search_back"], (get_pixel(img, points["search_back"])), 5):# if mine found
            print("mine found")
            if similar_color((45, 43, 37, 255), get_pixel(img, points["gather"]), 20):# if mine found and point gather is invisible
                print(True)
            else:# click on mine to get it visible
                print(False)
                click(points["mine"])
                sleep(1)
            click(points["mine"])
            sleep(2)
            gather_mine()
            print("gathering mine")
            witch_mine += 1
            return
        else:             # if mine not found
            if mine_type < 470:
                print("second type")
                mine_type += 162
            else:
                print("less lv")
                mine_type = 0
                lv += 1
            find_another()

def second_point_blue():
    global point_elite_blue
    point_elite_blue = (point_elite_blue, point_elite_blue[1] + 228)

def get_elite(farm):
    print("Elite")
    match farm:
        case 0 | 4:
            point_elite_mine = points["elite_mine1"]
            second_blue: bool = False
        case _:
            point_elite_mine = point_elite_blue
            second_blue: bool = True
    while True:
        click(points["favorites"])
        click(points["elite"])
        sleep(1)
        color = check_color(point_elite_mine)
        if color == (34, 108, 137, 255):# color of blue
            click(point_elite_mine)
            sleep(3)# too much but should work
            if not similar_color((144, 72, 51, 255), check_color(points["gather_elite"]), 10):# if elite isn't occupied by another alliance
                click(points["gather_elite"])
                sleep(1)
                color = check_color(points["vip"])
                if color != (0, 132, 162, 255):# if I don't need VIP # I think this color isn't True
                     if color == (55, 80, 18, 255):# if somebody is going to elite mine
                         click(points["vip"])
                     click(points["go"])# regularly I should be there
                     if second_blue:
                         second_point_blue()
                     return True# everything is alright I went to elite
                else:
                    wait()
                    wait()
                    click(points["back"])
                    return True# if I need VIP
            else:# if elite is occupied by someone
                print("someone else is already elite")
                if second_blue:
                    second_point_blue()# again while
                else:
                    return False
        else:
            print("some chemistry error", color)
            click(points["favourites_back"])
            return False# if there is no elites

def second_farm():
    global point_google, acc
    print("running second_farm")
    sleep(1)
    click(points["avatar"])
    sleep(1)
    click(points["account"])
    sleep(1)
    click(points["switch"])
    sleep(1)
    click(points["login"])
    sleep(1)
    click(points["google"])
    sleep(3)
    click(points["castle2"])
    sleep(1)
    click(points["confirm"])# go inside
    if not acc:
        point_google = (point_google[0], point_google[1] + 200)
    acc = not acc
    print("end second farm")
    sleep(20)# I can make the still checking there

def zeroing():
    global witch_mine
    witch_mine = 0
    # there can be zeroing lv (
