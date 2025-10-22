from .adb_device import device


def click(cords: tuple[int, int]) -> None:
    from subprocess import DEVNULL
    device.action(f"shell input tap {cords[0]} {cords[1]}", stdout=DEVNULL)


def screencap() -> str:
    from subprocess import PIPE
    result = device.action("exec-out screencap -p", stdout=PIPE)
    return result
