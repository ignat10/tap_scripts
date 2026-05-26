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

data = run(adb, capture_output=True)


# skip possible header if needed
# data = data[12:]

img = Image.frombytes("RGBA", (width, height), data.stdout)

img.save("screen.png")
