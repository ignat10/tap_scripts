from typing import Callable, TypeVar
from functools import wraps

from cv2 import imdecode, cvtColor, COLOR_BGR2GRAY, IMREAD_COLOR
from numpy import ndarray, frombuffer, uint8

from ..device.actions import screencap


temp_screen: ndarray | None = None


def reset_temp_screen() -> None:
    global temp_screen
    temp_screen = None


def _capture_screen() -> None:
    global temp_screen
    console_output =  screencap()
    screen_bytes = frombuffer(console_output, uint8)
    screen = imdecode(screen_bytes, IMREAD_COLOR)
    gray_screen = cvtColor(screen, COLOR_BGR2GRAY)
    temp_screen = gray_screen


R = TypeVar("R")
def with_screen(
        func: Callable[..., R]
        ) -> Callable[..., R]:
    @wraps(func)
    def wrapper(
        self,
        *args,
        **kwargs,
        ):
        if temp_screen is None:
            _capture_screen()
        return func(
            self,
            *args,
            screen=temp_screen,
            **kwargs
            )
    return wrapper
