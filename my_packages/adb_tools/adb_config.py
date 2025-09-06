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
        online = output.count("device") - 1
        offline = output.count("offline")
        devices = online + offline
        print(f"online: {online}, offline: {offline}:")
        match devices:
            case 0:
                clipboard = paste()
                if clipboard.find(IP) != -1:
                    print("connecting to device")
                    run(["adb", "connect", clipboard])
                else:
                    print(f"clipboard is '{clipboard}'\ncopy your ip")
            case 1 if online:
                break
            case _:
                run(["adb", "disconnect"])
        sleep(1)

    print("connected to device")