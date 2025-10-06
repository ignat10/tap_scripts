import cv2
from PIL import Image

from my_packages.core.adb_utils import make_screen
from my_packages.data.paths import screen_state_path, path


def _open_screen_pillow():
    make_screen()
    return Image.open(screen_state_path)


def _open_screen_cv2():
    make_screen()
    return cv2.imread(screen_state_path)


def check_color(point_checking: tuple[int, int]):
    return list[int](_open_screen_pillow().getpixel((point_checking[0], point_checking[1])))


def search_part(folder_name: str, gap: float, fullscreen=None):
    if fullscreen is None:
        fullscreen = _open_screen_cv2()
    else:
        fullscreen = cv2.imread(screen_state_path)

    max_val: float = 0
    for name in path[folder_name]:
        origin = cv2.imread(name)
        matched = cv2.matchTemplate(fullscreen, origin, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
        if max_val > gap:
            print(f"matched {name[-10:]} {max_val}/{gap}")
            return max_loc
    print(f"no matched {max_val}/{gap}")
    return None


def is_fullscreen(folder_name: str, gap: int) -> bool:
    fullscreen = _open_screen_cv2()
    for file in path[folder_name]:
        origin = cv2.imread(str(file))
        matched = cv2.PSNR(fullscreen, origin)
        if matched > gap:
            print(f"similarity :{matched}/{gap}")
            return True

    return False
