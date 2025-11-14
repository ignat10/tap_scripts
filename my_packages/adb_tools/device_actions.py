from .device_config import config


serial: str = config()


def action(arguments: str, **kwargs) -> str:
    from .console_runner import adb_run
    command = f"-s {serial} {arguments}"
    return adb_run(command, **kwargs)


def click(cords: tuple[int, int]) -> None:
    from subprocess import DEVNULL
    action(f"shell input tap {cords[0]} {cords[1]}", stdout=DEVNULL)


def screencap() -> str:
    from subprocess import PIPE
    return action("exec-out screencap -p", stdout=PIPE)
