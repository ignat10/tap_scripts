from subprocess import run
from time import sleep

from pyperclip import paste

IP = "192.168.0.1"

def console(command: list[str]) -> str:
        return run(
        command,
        capture_output=True,
        text=True,
    ).stdout

def connect_adb():
    print("connecting adb")

    while True:
        output = console(['adb', "devices"])
        print("stdout:", output)
        devices = output.count("device") - 1 + output.count("offline")
        print("devices:", devices)
        match devices:
            case 0:
                clipboard = paste()
                if clipboard.find(IP) != -1:
                    print("connecting to device")
                    run(["adb", "connect", clipboard])
                else:
                    print(f"copy your ip, now clipboard = {clipboard}")
            case 1:
                break
            case _:
                run(["adb", "disconnect"])
                print("disconnect")
        sleep(1)

    print("connected to device")