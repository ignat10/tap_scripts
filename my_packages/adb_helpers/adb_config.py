from time import sleep
import pyperclip

from my_packages.core.adb_device import find_device, connect_device
from my_packages.data.poco_coordinates import DEVICE_IP


def connect_adb() -> None:
    print("connecting adb")
    while True:
        device = find_device()
        if device is not None:
            break
        else:
            clipboard = pyperclip.paste()
            if clipboard.find(DEVICE_IP) != -1:
                print(f"connecting to device '{clipboard}'")
                if connect_device(clipboard):
                    continue
                else:
                    print(f"error connecting to device '{clipboard}'\nreset clipboard")
                    pyperclip.copy(None)
            else:
                print(f"clipboard is '{clipboard}'\ncopy your IP")
        sleep(1)

    print(f"connected to device '{device}'")
    return None
