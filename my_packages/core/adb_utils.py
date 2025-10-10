from .adb_console import adb_run
from .adb_device import device
from ..data.paths import screen_state_path


def adb_s(arguments: str, **kwargs) -> None:
    command = f"-s {device.device} {arguments}"
    adb_run(command, **kwargs)


def click(cords: tuple[int, int]) -> None:
    adb_s(f"shell input tap {cords[0]} {cords[1]}")


def make_screen() -> None:
    adb_s(f"exec-out screencap -p > {screen_state_path}", shell=True)
