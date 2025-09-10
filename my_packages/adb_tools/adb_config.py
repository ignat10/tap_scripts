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
    output = console(["adb, devices"])
    lines = output.splitlines()
    devices = []
    for line in lines:
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
        active_device = None
        for serial, status in devices:
            if status == "device":
                active_device = serial
                break

        match active_device:
            case 0:
                clipboard = paste()
                if clipboard.find(IP) != -1:
                    print("connecting to device")
                    run(["adb", "connect", clipboard])
                else:
                    print(f"clipboard is '{clipboard}'\ncopy your ip")
            case 1:
                break
            case _:
                pass
        sleep(1)

    print("connected to device")