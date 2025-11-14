import cv2

from numpy import ndarray, frombuffer, uint8

from ..adb_tools.device_actions import screencap

temp_screen: ndarray = ndarray([])

def _capture_gray() -> ndarray:
    global temp_screen
    console_output =  screencap()
    screen_bytes = frombuffer(console_output, uint8)
    screen = cv2.imdecode(screen_bytes, cv2.IMREAD_COLOR)
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    temp_screen = gray_screen
    return gray_screen


def get_screen( do_screen=True) -> ndarray:
    return _capture_gray() if do_screen else temp_screen if temp_screen is not None else exit("No temp screen captured") 