from cv2 import imdecode, cvtColor, COLOR_BGR2GRAY, IMREAD_COLOR
from numpy import ndarray, frombuffer, uint8



temp_screen: ndarray = None


def _capture_gray() -> ndarray:
    from ..adb_tools.adb_actions import screencap
    global temp_screen
    console_output =  screencap()
    screen_bytes = frombuffer(console_output, uint8)
    screen = imdecode(screen_bytes, IMREAD_COLOR)
    gray_screen = cvtColor(screen, COLOR_BGR2GRAY)
    temp_screen = gray_screen
    return gray_screen


def get_screen(do_screen: bool = True):
    return (
        _capture_gray() if do_screen 
        else temp_screen if temp_screen is not None 
        else exit("No temp screen captured")
    )
