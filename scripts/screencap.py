from dotenv import load_dotenv
from os import getenv
from subprocess import run

from PIL import Image

width = 720
height = 1280

load_dotenv()
adb = getenv("ADB")
if adb is None:
    raise ValueError("Please set ADB to .env file")

data = run([adb, "exec-out", "screencap"], capture_output=True).stdout



img = Image.frombytes("RGBA", (width, height), data)

img.save("screen.png")
