from subprocess import DEVNULL, PIPE


from ..adb_tools.console_runner import adb_run
from .config import configure_device
from ..game_object.point_obj import Coords



serial: str | None = None


def config_serial() -> None:
    global serial
    serial = configure_device()


def _action(arguments: str, **kwargs):
    if serial is None:
        config_serial()
    command = f"-s {serial} {arguments}"
    return adb_run(command, **kwargs)


def input_tap(coords: Coords) -> None:
    _action(f"shell input tap {coords.x} {coords.y}", stdout=DEVNULL)


def screencap() -> str:
    return _action("exec-out screencap -p", stdout=PIPE)
