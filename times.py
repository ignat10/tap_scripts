import time
import os
from PIL import Image
import subprocess


ADB = r"C:\Users\ignat\platform-tools\adb.exe"

point_search_back = (790, 1890)
point_close = (200, 1925)


# start = time.perf_counter()
# os.system(f"{ADB} shell input tap {point_close[0]} {point_close[1]}")
# end = time.perf_counter()
# print("1 click = ", end - start, "sec")  # 1,7 sec (0,7 just click)
while True:
    start = time.perf_counter()
    f = open("screen.png", "wb")  # should be done        with open("screen.png", "wb")
    subprocess.run([ADB, "exec-out", "screencap", "-p"], stdout = f)
    img = Image.open("screen.png")
    color = img.getpixel((point_search_back[0], point_search_back[1]))
    end = time.perf_counter()
    print("subprocess open screen + Image.open + get_pixel + ", end - start)
    print("color of back = ", color, "sec")