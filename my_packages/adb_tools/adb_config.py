from subprocess import run
from time import sleep

from pyperclip import paste

IP = "192.168.0.1"
_device_id = None

def console(command: list[str]) -> str:
        return run(
        command,
        capture_output=True,
        text=True,
    ).stdout

def list_devices() -> list[tuple]:
    output = console(["adb", "devices"])
    lines = output.splitlines()
    devices = []
    for line in lines[1::]:
        if line.strip():
            name, status = line.split("\t")
            devices.append((name, status))
    return devices

def connect_adb():
    global _device_id
    print("connecting adb")

    while True:
        devices = list_devices()
        print("devices:", devices)
        for serial, status in devices:
            if status == "device":
                _device_id = serial
                break

        print("active_device:", _device_id)
        if _device_id is not None:
            break
        else:
            clipboard = paste()
            if clipboard.find(IP) != -1:
                print("connecting to device")
                run(["adb", "connect", clipboard])
            else:
                print(f"clipboard is '{clipboard}'\ncopy your ip")
        sleep(1)

    print("connected to device")
    return _device_id

def get_device_name():
    if _device_id is None:
        return connect_adb()
    return _device_id