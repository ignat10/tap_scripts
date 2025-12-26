from subprocess import DEVNULL, PIPE


from .device_config import config
from .console_runner import adb_run



serial: str = config()


def action(arguments: str, **kwargs) -> str:
    command = f"-s {serial} {arguments}"
    return adb_run(command, **kwargs)


def input_tap(cords: tuple[int, int]) -> None:
    action(f"shell input tap {cords[0]} {cords[1]}", stdout=DEVNULL)


def screencap() -> str:
    return action("exec-out screencap -p", stdout=PIPE)
