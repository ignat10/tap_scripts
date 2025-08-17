# local
from my_packages import connect_adb
from my_packages.game_actions import *

# adb shell input tap 500 500

# ADB = r"D:\platform-tools\adb.exe"   #include ADB lenovo ( "C:\platform-tools\adb.exe" )
# add resolutions
REALME_7_RESOLUTION = (1080, 2400)
POCO_X7_PRO_RESOLUTION = (1220, 2712)

# add points to click as floats
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


#functions


# start script
connect_adb()

while True:
    print(check_color(points["search_back"]))