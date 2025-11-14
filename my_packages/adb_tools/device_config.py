from time import sleep

import pyperclip

from .console_runner import adb_run
from ..data.poco_coordinates import DEVICE_IP



def config() -> str:
    print("connecting adb")
    while not scan():
        clipboard = pyperclip.paste()
        if DEVICE_IP in clipboard:
            print(f"connecting to device '{clipboard}'")
            if connect(clipboard):
                continue
            else:
                print(f"error connecting to device '{clipboard}'\nreset clipboard")
                pyperclip.copy("")
        else:
            print(f"clipboard is '{clipboard}'\ncopy your IP")
        sleep(1)


def scan() -> str | None:
    output = adb_run("devices", capture_output=True, text=True)
    lines: list[str] = output.splitlines()
    for line in lines[1::]:
        if line.strip():
            name, status = line.split()
            if status == "device":
                return name
    return None


def connect(device: str) -> bool:
    output = adb_run(f"connect {device}", capture_output=True, text=True)
    success: bool = f"connected" in output
    return success
