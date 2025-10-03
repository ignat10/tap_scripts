from os import system
from subprocess import run

from my_packages.data.paths import screen_state_path

device = None


def adb(arguments: str) -> None:
    system(f"adb {arguments}")


def adb_s(arguments: str) -> None:
    adb(f"-s {device} {arguments}")

def adb_run(arguments: str) -> str:
    cmd = f"adb {arguments}"
    print(f"running: {cmd}")
    output = run(cmd,
                 shell=True,
                 capture_output=True,
                 text=True
                 )
    return output.stdout


def click(cords: tuple[int, int]):
    adb_s(f"shell input tap {cords[0]} {cords[1]}")


def make_screen():
    adb_s(f"exec-out screencap -p > {screen_state_path}")


def find_device() -> str | None:
    global device
    output = adb_run("devices")
    lines: list[str] = output.splitlines()
    devices: list[tuple[str, str]] = []
    for line in lines[1::]:
        if line.strip():
            name, status = line.split("\t")
            devices.append((name, status))
    for serial, status in devices:
        if status == "device":
            device = serial
            return device
    return None


def connect_device(serial: str):
    output = adb_run(f"connect {serial}")
    is_success: bool = output.find(f"connected to {serial}") == 1
    return is_success
