from subprocess import DEVNULL, PIPE


from ..adb_tools.console_runner import adb_run
from .config import configure_device



serial: str | None = None


def config_serial() -> None:
    global serial
    serial = configure_device()


def _action(arguments: str, **kwargs):
    command = f"-s {serial} {arguments}"
    return adb_run(command, **kwargs)


def input_tap(cords: tuple[int, int]) -> None:
    _action(f"shell input tap {cords[0]} {cords[1]}", stdout=DEVNULL)


def screencap() -> str:
    return _action("exec-out screencap -p", stdout=PIPE)
