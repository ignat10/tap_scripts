import time
import os
from PIL import Image
import subprocess
# import cv2


ADB = r"C:\Users\ignat\platform-tools\adb.exe"   #include ADB lenovo ( "C:\platform-tools\adb.exe" )


# add points to click
point_take = (520, 1690)
point_close = (200, 1925)
point_lord = (1000, 1830)
point_harvest = (200, 1560)
point_use = (530, 2330)
point_map = (100, 2300)
point_search = (1000, 1981)
point_iron = (600, 2075)# point stone, wood, food = (600, 425, 256, 100,   2075)  --162
point_stone = (425, 2075)
point_wood = (256, 2075)
point_food = (100, 2075)
point_plus = (675, 2310)
point_minus = (115, 2310)
point_go_mine = (900, 2325)
point_search_back = (786, 1840)
point_mine = (545, 1185)
point_gather = (775, 1158)
point_go = (900, 2315)
point_back = (790, 2121)
point_favorites = (70, 1823)
point_favourites_back = (70, 150)
point_elite = (700, 365)
point_elite_blue = (380, 785) # point_elite_blue2, 3, 4, 5 = (380 1015, 1230, 1460, 1690) ++228
point_elite_mine1 = (380, 785)
point_gather_elite = (780, 930)
point_vip = (891, 1411)
point_avatar = (90, 228)
point_account = (180, 1100)
point_switch = (550, 1600)
point_login = (560, 1320)
point_google = (145, 930)  # google 1,2,3,4,5 y = 730, 930, 1130, 1330, 1530
point_castle1 = (400, 1000)
point_castle2 = (400, 1100)
point_confirm = (313, 1372)


lv = 0 # iron first than - that
mine_type = 0# 6 lv minus that number
witch_mine = 0
acc: bool = True

#functions
def click(cords: (int, int)):
    os.system(f"{ADB} shell input tap {cords[0]} {cords[1]}")

def wait():
    time.sleep(0.5)
    click(point_close)

def make_screen():
    with open(f"screen.png", "wb") as f:
        subprocess.run([ADB, "exec-out", "screencap", "-p"], stdout = f)
    return Image.open("screen.png")

def get_pixel(screen, cords):
    return screen.getpixel(cords)

def check_color(point_checking: (int, int)):
    return make_screen().getpixel((point_checking[0], point_checking[1]))

def similar_color(color: (int, int, int, int), another_color: (int, int, int, int), tolerance: int) -> bool:
    return all(abs(a - t < tolerance) for a, t in zip(another_color, color))

def harvest():
    print("Harvesting...")
    time.sleep(0.5)
    click(point_lord)
    time.sleep(0.5)
    click(point_harvest)
    time.sleep(0.5)
    click(point_use)
    print("end harvest")
    wait()
    wait()

def inside():
    print("running inside")                        # Inside the castle
    # click(point_take)  # take daily gift
    for _ in range(4):  # close ad (4 times close)
        wait()  # close ad
    harvest()
    click(point_map)
    print("running outside")
    time.sleep(2)

def find_another():# to find another mine if not found
    global mine_type, lv
    os.system(f"{ADB} shell input tap {point_iron[0] - mine_type} {point_iron[1]}")
    time.sleep(0.5)
    for _ in range(5):
        click(point_plus)
    for _ in range(lv):
        click(point_minus)
        time.sleep(0.5)
    for _ in range(3):
        click(point_go_mine)
    time.sleep(2)

def gather_mine():
    click(point_gather)
    if witch_mine < 3:
        if check_color(point_vip) == (0, 132, 162, 255):# if I don't have free march
            wait()
            wait()
            return
    click(point_go)
    click(point_back)

def get_mine(): # to go to basic mine from the map
    global mine_type, lv, witch_mine
    click(point_search)
    find_another()
    while True:
        img = make_screen()
        if similar_color((40, 36, 34, 255), (get_pixel(img, point_search_back)), 5):# if mine found
            print("mine found")
            if similar_color((45, 43, 37, 255), get_pixel(img, point_gather), 20):# if mine found and point gather is invisible
                print(True)
            else:# click on mine to get it visible
                print(False)
                click(point_mine)
                time.sleep(1)
            click(point_mine)
            time.sleep(2)
            gather_mine()
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
            point_elite_mine = point_elite_mine1
            second_blue: bool = False
        case _:
            point_elite_mine = point_elite_blue
            second_blue: bool = True
    while True:
        click(point_favorites)
        click(point_elite)
        time.sleep(1)
        color = check_color(point_elite_mine)
        if color == (34, 108, 137, 255):# color of blue
            click(point_elite_mine)
            time.sleep(3)# too much but should work
            if not similar_color((144, 72, 51, 255), check_color(point_gather_elite), 10):# if elite isn't occupied by another alliance
                click(point_gather_elite)
                time.sleep(1)
                color = check_color(point_vip)
                if color != (0, 132, 162, 255):# if I don't need VIP # I think this color isn't True
                     if color == (55, 80, 18, 255):# if somebody is going to elite mine
                         click(point_vip)
                     click(point_go)# regularly I should be there
                     if second_blue:
                         second_point_blue()
                     return True# everything is alright I went to elite
                else:
                    wait()
                    wait()
                    click(point_back)
                    return True# if I need VIP
            else:# if elite is occupied by someone
                print("someone else is already elite")
                if second_blue:
                    second_point_blue()# again while
                else:
                    return False
        else:
            print("some chemistry error", color)
            click(point_favourites_back)
            return False# if there is no elites

def second_farm():
    global point_google, acc
    print("running second_farm")
    time.sleep(1)
    click(point_avatar)
    time.sleep(1)
    click(point_account)
    time.sleep(1)
    click(point_switch)
    time.sleep(1)
    click(point_login)
    time.sleep(1)
    click(point_google)
    time.sleep(3)
    click(point_castle2)
    time.sleep(1)
    click(point_confirm)# go inside
    if not acc:
        point_google = (point_google[0], point_google[1] + 200)
    acc = not acc
    print("end second farm")
    time.sleep(20)# I can make the still checking there

def zeroing():
    global witch_mine
    witch_mine = 0
    # there can be zeroing lv (

# start script
for castle in range(7):
    inside()

    for _ in range(2):
        get_mine()

    if not get_elite(castle):
        get_mine()
    get_mine()

    second_farm()
    zeroing()