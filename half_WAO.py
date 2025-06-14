import time
import os
from PIL import Image
import subprocess


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
point_elite_mine = (380, 785) # point_elite_mine2, 3, 4, 5 = (380 1015, 1230, 1460, 1690) ++228
point_elite2 = (380, 1015)
point_elite3 = (380, 1242)
point_elite4 = (380, 1470)
point_elite5 = (380, 1699)
point_gather_elite = (780, 930)
point_vip = (891, 1411)
point_avatar = (90, 228)
point_account = (180, 1100)
point_switch = (550, 1528)
point_login = (560, 1320)
point_google = (145, 930)  # google 1,2,3,4,5 y = 730, 930, 1130, 1330, 1530
point_castle1 = (400, 1000)
point_castle2 = (400, 1100)
point_confirm = (313, 1372)

# 6 lv minus that number
img = None
lv = 0 # iron first than - that
mine_type = 0
witch_mine = 0
acc = 1

#functions
def click(cords):
    os.system(f"{ADB} shell input tap {cords[0]} {cords[1]}")

def wait():
    time.sleep(0.5)
    os.system(f"{ADB} shell input tap {point_close[0]} {point_close[1]}")

def check_color(point_checking):
    global img
    f = open(f"screen.png", "wb")
    subprocess.run([ADB, "exec-out", "screencap", "-p"], stdout = f)
    img = Image.open("screen.png")
    return img.getpixel((point_checking[0], point_checking[1]))

def find_another():# to find another mine if not found
    global mine_type, lv
    os.system(f"{ADB} shell input tap {point_iron[0] - mine_type} {point_iron[1]}")
    time.sleep(0.5)
    for k in range(5):
        os.system(f"{ADB} shell input tap {point_plus[0]} {point_plus[1]}")
    for j in range(lv):
        os.system(f"{ADB} shell input tap {point_minus[0]} {point_minus[1]}")
        time.sleep(0.5)
    for l in range(3):
        os.system(f"{ADB} shell input tap {point_go_mine[0]} {point_go_mine[1]}")
    time.sleep(1)

def gather_mine():
    click(point_mine)
    time.sleep(1)
    os.system(f"{ADB} shell input tap {point_gather[0]} {point_gather[1]}")
    if witch_mine < 3:
        if not check_color(point_vip) == (0, 132, 162, 255):
            os.system(f"{ADB} shell input tap {point_go[0]} {point_go[1]}")
            os.system(f"{ADB} shell input tap {point_back[0]} {point_back[1]}")
        else:
            wait()
            wait()

def get_mine(): # to go to basic mine from the map
    global mine_type, lv, witch_mine
    os.system(f"{ADB} shell input tap {point_search[0]} {point_search[1]}")
    find_another()
    while True:
        if all(abs(a - t) < 5 for a, t in zip(check_color(point_search_back), (40, 36, 34, 255))):# if mine found
            print("mine found")
            if all(abs(a - t) < 20 for a, t in zip(check_color(point_gather), (45, 43, 37, 255))):# tuple of color gather mine # if mine found and gather is visible
                gather_mine()
                break
            else:# if mine found but point gather is invisible
                os.system(f"{ADB} shell input tap {point_mine[0]} {point_mine[1]}")
                time.sleep(0.5)
                print(True if all(abs(a - t) < 20 for a, t in zip(check_color(point_gather), (45, 43, 37, 255))) else False)
                gather_mine()
        else:             # if mine not found
            if mine_type < 470:
                mine_type += 162
            else:
                mine_type = 0
                lv += 1
            find_another()
    witch_mine += 1

def get_elite():
    global point_elite_mine
    while True:
        os.system(f"{ADB} shell input tap {point_favorites[0]} {point_favorites[1]}")
        os.system(f"{ADB} shell input tap {point_elite[0]} {point_elite[1]}")
        time.sleep(1)

        if check_color(point_elite_mine) == (34, 108, 137, 255):# color of blue
            os.system(f"{ADB} shell input tap {point_elite_mine[0]} {point_elite_mine[1]}")
            time.sleep(3)# too much but should work
            color = check_color(point_gather_elite)
            if not all(abs(a - t) < 10 for a, t in zip(color, (144, 72, 51, 255))):# if elite isn't occupied by another alliance
                os.system(f"{ADB} shell input tap {point_gather_elite[0]} {point_gather_elite[1]}")
                time.sleep(1)
                color = check_color(point_vip)

                if not color == (0, 132, 162, 255):# if castle can go 19 # I think this color isn't True
                     if color == (55, 80, 18, 255):# if somebody is going to elite mine
                         click(point_vip)
                     click(point_go)
                     return 0
                else:
                    wait()
                    wait()
                    click(point_back)
                    return 3
            else:# if elite is occupied by someone
                point_elite_mine = (point_elite_mine[0], point_elite_mine[1] + 228)
        else:
            print("some chemistry error", check_color(point_elite_mine))
            os.system(f"{ADB} shell input tap {point_favourites_back[0]} {point_favourites_back[1]}")
            return 1

def second_farm():
    global point_google, acc
    acc = 2
    os.system(f"{ADB} shell input tap {point_avatar[0]} {point_avatar[1]}")
    time.sleep(1)
    os.system(f"{ADB} shell input tap {point_account[0]} {point_account[1]}")
    while True:
        time.sleep(1)
        os.system(f"{ADB} shell input tap {point_switch[0]} {point_switch[1]}")
        time.sleep(1)
        os.system(f"{ADB} shell input tap {point_login[0]} {point_login[1]}")
        time.sleep(1)
        os.system(f"{ADB} shell input tap {point_google[0]} {point_google[1]}")
        time.sleep(1)
        if acc == 1:
            os.system(f"{ADB} shell input tap {point_castle1[0]} {point_castle1[1]}")
            acc = 2
            break
        else:        # if 1 acc is used
            if check_color(point_castle2) == (42, 74, 102, 255):# if 2 acc exists
               os.system(f"{ADB} shell input tap {point_castle2[0]} {point_castle2[1]}")# go inside
               break
            else:   # if 2 acc is not exists
                wait()# close menu
            acc = 1
            point_google = (145, point_google[1] + 200)# second google acc
    os.system(f"{ADB} shell input tap {point_confirm[0]} {point_confirm[1]}")

#start
get_elite()