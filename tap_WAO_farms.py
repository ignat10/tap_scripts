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
point_search_back = (790, 1890)
point_mine = (545, 1185)
point_gather = (775, 1158)
point_go = (900, 2315)
point_back = (790, 2121)
point_favorites = (70, 1823)
point_favourites_back = (70, 1823)
point_elite = (700, 365)
point_elite_mine = (380, 785) # point_elite_mine2, 3, 4, 5 = (380 1015, 1230, 1460, 1690) ++228
point_elite2 = (380, 1015)
point_elite3 = (380, 1242)
point_elite4 = (380, 1470)
point_elite5 = (380, 1699)
point_gather_elite = (770, 940)
point_vip = (900, 1455)
point_avatar = (90, 228)
point_account = (180, 1100)
point_switch = (550, 1528)
point_login = (560, 1360)
point_google = (145, 790)  # google 2,3,4,5 y = 930, 1130, 1330, 1530
point_castle1 = (400, 1000)
point_castle2 = (400, 1100)
point_confirm = (313, 1372)

# 6 lv minus that number
lv = 0 # iron first than - that
mine_type = 0
color = 0
witch_mine = 0
acc = 1

#functions
def wait():
    time.sleep(0.5)
    os.system(f"{ADB} shell input tap {point_close[0]} {point_close[1]}")

def check_color(point_checking):
    global color
    f = open(f"screen.png", "wb")
    subprocess.run([ADB, "exec-out", "screencap", "-p"], stdout = f)
    img = Image.open("screen.png")
    color = img.getpixel((point_checking[0], point_checking[1]))
    print("color of checking point", color)  # debug

def find_another():
    global mine_type, lv
    os.system(f"{ADB} shell input tap {point_search[0]} {point_search[1]}")
    time.sleep(0.5)
    os.system(f"{ADB} shell input tap {point_iron[0] - mine_type} {point_iron[1]}")
    time.sleep(0.5)
    for k in range(5):
        os.system(f"{ADB} shell input tap {point_plus[0]} {point_plus[1]}")
    for j in range(lv):
        os.system(f"{ADB} shell input tap {point_minus[0]} {point_minus[1]}")
        time.sleep(0.5)
    os.system(f"{ADB} shell input tap {point_go_mine[0]} {point_go_mine[1]}")
    time.sleep(1)

def gather_mine():
    os.system(f"{ADB} shell input tap {point_gather[0]} {point_gather[1]}")
    if witch_mine > 3:
        check_color(point_vip)
        if not color == (0, 132, 162, 255):
            os.system(f"{ADB} shell input tap {point_go[0]} {point_go[1]}")
            os.system(f"{ADB} shell input tap {point_back[0]} {point_back[1]}")
        else:
            wait()
            wait()

def get_mine(): # to go to basic mine from the map
    global mine_type, color, lv, witch_mine
    os.system(f"{ADB} shell input tap {point_search[0]} {point_search[1]}")  # At the map
    find_another()
    while True:
        check_color(point_search_back)
        if all(abs(a - t) < 5 for a, t in zip(color, (50, 45, 35, 255))):  # put #(XXX, XXX, XXX)
            check_color(point_gather)
            wait()
            if all(abs(a - t) < 5 for a, t in zip(color, (46, 37, 43, 255))):
                wait()
                gather_mine()
                break
            else:
                os.system(f"{ADB} shell input tap {point_mine[0]} {point_mine[1]}")
                gather_mine()
                break
        else:
            find_another()
            check_color(point_gather)
            if all(abs(a - t) < 5 for a, t in zip(color, (46, 37, 43, 255))):# put #(XXX, XXX, XXX) # I think that is good color                             # if found
                wait()
                gather_mine()
                break
            else:
                wait()
                os.system(f"{ADB} shell input tap {point_mine[0]} {point_mine[1]}")
                check_color(point_gather)    # check color of point_gather
                if all(abs(a - t) < 5 for a, t in zip(color, (46, 37, 43, 255))):
                    gather_mine()
                    break
                else:           # if not found
                    if mine_type < 470:
                        mine_type += 162
                    else:
                        mine_type = 0
                        lv += 1
                    find_another()
    witch_mine += 1

def second_farm():
    global point_google, acc
    acc = 1
    point_google = (145, 790)  # google 2,3,4,5 y = 930, 1130, 1330, 1530
    os.system(f"{ADB} shell input tap {point_avatar[0]} {point_avatar[1]}")
    os.system(f"{ADB} shell input tap {point_account[0]} {point_account[1]}")
    while True:
        os.system(f"{ADB} shell input tap {point_switch[0]} {point_switch[1]}")
        os.system(f"{ADB} shell input tap {point_login[0]} {point_login[1]}")
        time.sleep(1)
        os.system(f"{ADB} shell input tap {point_google[0]} {point_google[1]}")
        if acc == 1:
            os.system(f"{ADB} shell input tap {point_castle1[0]} {point_castle1[1]}")
            acc = 2
            break
        else:        # if 1 acc is used
            check_color(point_castle2)
            if color == (42, 74, 102, 255):# if 2 acc exists
               os.system(f"{ADB} shell input tap {point_castle2[0]} {point_castle2[1]}")# go inside
               break
            else:   # if 2 acc is not exists
                wait()# close menu
            acc = 1
            point_google = (145, point_google[1] + 200)# second google acc
    os.system(f"{ADB} shell input tap {point_confirm[0]} {point_confirm[1]}")



# start script
for farm in range(8):
    os.system(f"{ADB} shell input tap {point_take[0]} {point_take[1]}") # take daily gift                        # Inside the castle
    for i in range(3):# close ad (3 times close)
        wait()        # close ad
    os.system(f"{ADB} shell input tap {point_lord[0]} {point_lord[1]}")
    os.system(f"{ADB} shell input tap {point_harvest[0]} {point_harvest[1]}")
    os.system(f"{ADB} shell input tap {point_use[0]} {point_use[1]}")
    for i in range(2):
        wait()
    os.system(f"{ADB} shell input tap {point_map[0]} {point_map[1]}")
    time.sleep(5)

    for i in range(3):
        get_mine()





    os.system(f"{ADB} shell input tap {point_favorites[0]} {point_favorites[1]}")
    os.system(f"{ADB} shell input tap {point_elite[0]} {point_elite[1]}")

    check_color(point_elite_mine)
    if all(abs(a - t) < 5 for a, t in zip(color, (34, 108, 137, 255))): # line up, color = (XXX, XXX, XXX)
        os.system(f"{ADB} shell input tap {point_elite_mine[0]} {point_elite_mine[1]}")
        time.sleep(0.5)
        os.system(f"{ADB} shell input tap {point_gather_elite[0]} {point_gather_elite[1]}")
        check_color(point_vip)# activate vip
        if not color == (0, 132, 162, 255):# if castle => 19
            os.system(f"{ADB} shell input tap {point_go[0]} {point_go[1]}")
            point_elite_mine = (point_elite_mine[0], point_elite_mine[1] + 228)
        else:
            wait()
            wait()
    else:
        print("some chemistry error")
        os.system(f"{ADB} shell input tap {point_favourites_back[0]} {point_favourites_back[1]}")
        os.system(f"{ADB} shell input tap {point_search[0]} {point_search[1]}")
        get_mine()
    second_farm()