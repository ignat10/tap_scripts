import time
import os
from PIL import Image


ADB = r"C:\platform-tools\adb.exe"  #include ADB


# add points to click
point_take = (520, 1690)
point_close = (200, 1925)
point_help = (1000, 2100)
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
point_gather = (775, 1158)
point_go = (900, 2315)
point_favorites = (70, 1823)
point_elite = (700, 365)
point_elite_mine = (380, 780) # point_elite_mine2, 3, 4, 5 = (380 1010, 1230, 1460, 1690) ++230
point_elite2 = (380, 1010)
point_elite3 = (380, 1230)
point_elite4 = (380, 1460)
point_elite5 = (380, 1690)
point_gather_elite = (770, 940)
point_avatar = (90, 228)
point_account = (180, 1100)
point_switch = (550, 1528)
point_login = (560, 1360)
point_google = (145, 790)  #google 2,3,4,5 y = 930, 1130, 1330, 1530
point_castle1 = (500, 1000)
point_castle2 = (500, 1100)
point_confirm = (313, 1372)

# 6 lv minus that number
lv = 0 # iron first than - that
mine_type = 0

#functions
def wait():
    time.sleep(1)
    os.system(f"{ADB} shell input tap {point_close[0]} {point_close[1]}")

def find_another():
    global mine_type
    global lv
    os.system(f"{ADB} shell input tap {point_iron[0] - mine_type} {point_iron[1]}")
    time.sleep(0.5)
    for k in range(5):
        os.system(f"{ADB} shell input tap {point_plus[0]} {point_plus[1]}")
        time.sleep(0.1)
    for j in range(lv):
        os.system(f"{ADB} shell input tap {point_minus[0]} {point_minus[1]}")
        time.sleep(0.5)
    os.system(f"{ADB} shell input tap {point_go_mine[0]} {point_go_mine[1]}")
    time.sleep(2)

def get_mine(): # to go to basic mine from the map
    global mine_type
    global lv
    os.system(f"{ADB} shell input tap {point_search[0]} {point_search[1]}")  # At the map
    time.sleep(0.5)
    while True:
        if color == (46, 37, 43, 255):  # put #(XXX, XXX, XXX) # I think that is good color
            wait()                                       # if found
            os.system(f"{ADB} shell input tap {point_gather[0]} {point_gather[1]}")
            time.sleep(1)
            os.system(f"{ADB} shell input tap {point_go[0]} {point_go[1]}")
            lv = 0
            mine_type = 0
            break
        else:                                                # if not found
            find_another()
            os.system("adb exec-out screencap -p > screen.png")
            time.sleep(1)
            img = Image.open("screen.png")
            color = img.getpixel((point_gather[0], point_gather[1]))
            print("color of gather if found mine", color)  # it to line down to know that mine found
            if mine_type < 470:
                mine_type += 162
            else:
                mine_type = 0
                lv += 1

# start script
os.system(f"{ADB} shell input tap {point_take[0]} {point_take[1]}") # take daily gift                        # Inside the castle
for i in range(4):#close ad (4 times close)
    wait()        # close ad
os.system(f"{ADB} shell input tap {point_help[0]} {point_help[1]}") # alliance help
time.sleep(1)
os.system(f"{ADB} shell input tap {point_lord[0]} {point_lord[1]}")
time.sleep(0.5)
os.system(f"{ADB} shell input tap {point_harvest[0]} {point_harvest[1]}")
time.sleep(0.5)
os.system(f"{ADB} shell input tap {point_use[0]} {point_use[1]}")
for i in range(2):
    wait()
time.sleep(1)
os.system(f"{ADB} shell input tap {point_map[0]} {point_map[1]}")
time.sleep(5)

for i in range(3):
    get_mine()
    lv = 0
    mine_type = 0






os.system(f"{ADB} shell input tap {point_favorites[0]} {point_favorites[1]}")
time.sleep(0.5)
os.system(f"{ADB} shell input tap {point_elite[0]} {point_elite[1]}")
time.sleep(0.5)

os.system("adb shell screencap -p /sdcard/screen.png") #

os.system("adb pull /sdcard/screen.png")

img = Image.open("screen.png")

color = img.getpixel((point_elite_mine[0], point_elite_mine[1]))
print(color) # just debug to know what number should I put up

if color == color: # line up, color = (XXX, XXX, XXX)
    os.system(f"{ADB} shell input tap {point_elite_mine[0]} {point_elite_mine[1]}")
    time.sleep(1)
    os.system(f"{ADB} shell input tap {point_gather_elite[0]} {point_gather_elite[1]}")
    time.sleep(0.5)
    os.system(f"{ADB} shell input tap {point_go[0]} {point_go[1]}")
    print("point elite mine", point_elite_mine) # that and second print for debug (++230)
    point_elite_mine = (point_elite_mine[0], point_elite_mine[1] + 230)
    print("point elite mine", point_elite_mine)
else:
    print("some chemistry error")

