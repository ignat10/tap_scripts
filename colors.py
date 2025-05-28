import time
import os
from PIL import Image

ADB = r"C:\platform-tools\adb.exe"

point_gather = (775, 1158)

os.system("adb exec-out screencap -p > screen.png")
time.sleep(2)
img = Image.open("screen.png")
time.sleep(2)
color = img.getpixel((point_gather[0], point_gather[1]))
print(color)