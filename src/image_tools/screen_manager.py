from cv2 import imdecode, cvtColor, COLOR_BGR2GRAY, IMREAD_COLOR
from numpy import ndarray, frombuffer, uint8


from ..device.actions import screencap


temp_screen: ndarray = None


def _capture_gray() -> ndarray:
    global temp_screen
    console_output =  screencap()
    screen_bytes = frombuffer(console_output, uint8)
    screen = imdecode(screen_bytes, IMREAD_COLOR)
    gray_screen = cvtColor(screen, COLOR_BGR2GRAY)
    temp_screen = gray_screen
    return gray_screen


def with_screen(func):
    def wrapper(
        self,
        do_screen: bool = True,
        *args,
        **kwargs
        ) -> ndarray:
        if do_screen:
            screen = _capture_gray()
        elif temp_screen is not None:
            screen = temp_screen
        else:
            raise RuntimeError("No temp screen captured")
        return func(self, *args, **kwargs, screen=screen)
    return wrapper
