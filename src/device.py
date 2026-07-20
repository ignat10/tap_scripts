from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from screen_objects import device_config


def config():
    load_dotenv()
    adb = getenv("ADB")
    ip = getenv("IP")
    if adb is None:
        raise Exception("ADB not set. set adb path in .env file.")
    device_config(adb=Path(adb), ip=ip)
