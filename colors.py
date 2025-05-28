import time
import os
from PIL import Image

ADB = r"C:\platform-tools\adb.exe"

point_gather = (775, 1158)

os.system("adb shell screencap -p /sdcard/screen.png")
time.sleep(5)
os.system("adb pull /sdcard/screen.png")
time.sleep(5)
img = Image.open("screen.png")
time.sleep(5)
color = img.getpixel((point_gather[0], point_gather[1]))
print(color)