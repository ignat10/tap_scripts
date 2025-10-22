from time import sleep
import pyperclip

from my_packages.core.adb_device import device
from my_packages.data.poco_coordinates import DEVICE_IP


def connect_adb() -> None:
    print("connecting adb")
    while True:
        device.find()
        if device.device is not None:
            break
        else:
            clipboard = pyperclip.paste()
            if DEVICE_IP in clipboard:
                print(f"connecting to device '{clipboard}'")
                device.connect(clipboard)
                if device.is_connected:
                    continue
                else:
                    print(f"error connecting to device '{clipboard}'\nreset clipboard")
                    pyperclip.copy("")
            else:
                print(f"clipboard is '{clipboard}'\ncopy your IP")
        sleep(1)
    print(f"connected to device '{device.device}'")
