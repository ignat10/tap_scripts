from typing import Callable, TypeVar, ParamSpec, Concatenate
from functools import wraps

from PIL import Image
import io
import numpy as np
from ..device.actions import screencap


temp_screen: np.ndarray | None = None


def reset_temp_screen() -> None:
    global temp_screen
    temp_screen = None


def _capture_screen() -> None:
    global temp_screen
    console_output = screencap()
    io_bytes = io.BytesIO(console_output)
    screen = Image.open(io_bytes)
    gray_screen = screen.convert("L")
    numpy_array = np.array(gray_screen, dtype=np.uint8)
    temp_screen = numpy_array

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")

def with_screen(
        func: Callable[Concatenate[T, np.ndarray, P], R]
        ) -> Callable[Concatenate[T, P], R]:
    @wraps(func)
    def wrapper(
        self,
        *args: P.args,
        **kwargs: P.kwargs,
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
