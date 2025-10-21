def adb_s(arguments: str, **kwargs) -> None:
    from .adb_device import device
    from .adb_console import adb_run
    command = f"-s {device.device} {arguments}"
    adb_run(command, **kwargs)


def click(cords: tuple[int, int]) -> None:
    adb_s(f"shell input tap {cords[0]} {cords[1]}")


def make_screen() -> None:
    from ..data.paths import path
    adb_s(f"exec-out screencap -p > {path.screen_state_path}", shell=True)


def adb_screencap() -> str:
    from .adb_console import adb_run
    from subprocess import PIPE
    result = adb_run("exec-out screencap -p", stdout=PIPE)
    return result
