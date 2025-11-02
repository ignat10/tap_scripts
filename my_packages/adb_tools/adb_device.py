from time import sleep

import pyperclip

from my_packages.core.adb_console import adb_run
from my_packages.data.poco_coordinates import DEVICE_IP


class AdbDevice:
    def __init__(self):
        self.device = None
        self.is_connected = None


    def find(self):
        output = adb_run("devices", capture_output=True, text=True)
        if output is not None:
            lines: list[str] = output.splitlines()
            devices: list[tuple[str, str]] = []
            for line in lines[1::]:
                if line.strip():
                    name, status = line.split()
                    devices.append((name, status))
            for serial, status in devices:
                if status == "device":
                    self.device = serial
                    break

    def connect(self, dev: str) -> None:
        output = adb_run(f"connect {dev}", capture_output=True, text=True)
        success: bool = f"connected" in output
        print(f"success connection: {success}")
        self.is_connected = success

    def connect_adb(self) -> None:
        print("connecting adb")
        while True:
            self.find()
            if self.device is not None:
                break
            else:
                clipboard = pyperclip.paste()
                if DEVICE_IP in clipboard:
                    print(f"connecting to device '{clipboard}'")
                    self.connect(clipboard)
                    if self.is_connected:
                        continue
                    else:
                        print(f"error connecting to device '{clipboard}'\nreset clipboard")
                        pyperclip.copy("")
                else:
                    print(f"clipboard is '{clipboard}'\ncopy your IP")
            sleep(1)
        print(f"connected to device '{self.device}'")

    def action(self, arguments: str, **kwargs) -> str:
        command = f"-s {self.device} {arguments}"
        return adb_run(command, **kwargs)

    def click(self, cords: tuple[int, int]) -> None:
        from subprocess import DEVNULL
        self.action(f"shell input tap {cords[0]} {cords[1]}", stdout=DEVNULL)

    def screencap(self) -> str:
        from subprocess import PIPE
        return self.action("exec-out screencap -p", stdout=PIPE)

device = AdbDevice()