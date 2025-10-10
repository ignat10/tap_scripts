import cv2
from PIL import Image

from my_packages.core.adb_utils import make_screen
from my_packages.data.paths import screen_state_path, build_full_path_list


def _open_screen_pillow():
    make_screen()
    return Image.open(screen_state_path)


def _open_screen_cv2():
    make_screen()
    return cv2.imread(screen_state_path)


def check_color(point_checking: tuple[int, int]) -> list[int]:
    return list[int](_open_screen_pillow().getpixel((point_checking[0], point_checking[1])))


def search_part(folder_name: str, gap: float, fullscreen=None) -> tuple[int, int] | None:
    if fullscreen is None:
        fullscreen = _open_screen_cv2()
    else:
        fullscreen = cv2.imread(screen_state_path)

    examples: list[str] = build_full_path_list(folder_name)
    max_val: float = 0
    for image in examples:
        origin = cv2.imread(image)
        matched = cv2.matchTemplate(fullscreen, origin, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(matched)
        if max_val > gap:
            print(f"matched {image[-10:]} {max_val}/{gap}")
            return tuple[int, int](max_loc)
    print(f"no matched {max_val}/{gap}")
    return None


def is_fullscreen(folder_name: str, gap: int) -> bool:
    fullscreen = _open_screen_cv2()
    examples: list[str] = build_full_path_list(folder_name)

    matched: float = 0
    for image in examples:
        origin = cv2.imread(image)
        matched = cv2.PSNR(fullscreen, origin)
        if matched > gap:
            print(f"similarity :{matched}/{gap}")
            return True
    print(f"no matched. max result: {matched}/{gap}")
    return False
