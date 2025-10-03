from time import sleep

from pyperclip import paste

from my_packages.core.adb_console import find_device, connect_device

IP = "192.168.0.1"


def connect_adb():
    print("connecting adb")
    while True:
        device = find_device()
        if device is not None:
            break
        else:
            clipboard = paste()
            if clipboard.find(IP) != -1:
                print(f"connecting to device '{clipboard}'")
                connect_device(clipboard)
            else:
                print(f"clipboard is '{clipboard}'\ncopy your IP")
        sleep(1)

    print(f"connected to device '{device}'")
