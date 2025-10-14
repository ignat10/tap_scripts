import cv2
from PIL import Image
from skimage.metrics import structural_similarity as ssim

from my_packages.core.adb_utils import make_screen
from my_packages.data.paths import screen_state_path, build_full_paths


def _get_pillow_screen():
    make_screen()
    return Image.open(screen_state_path)


def _read_temp_screen():
    return cv2.imread(screen_state_path)


def _get_cv2_screen():
    make_screen()
    return _read_temp_screen()


def check_color(point_checking: tuple[int, int]) -> list[int]:
    return list(_get_pillow_screen().getpixel((point_checking[0], point_checking[1])))


def search_part(folder_name: str, gap: float, fullscreen=None) -> tuple[int, int] | None:
    fullscreen = _read_temp_screen() if fullscreen is not None else _get_cv2_screen()

    examples: list[str] = build_full_paths(folder_name)
    max_val: float = 0.0
    for image in examples:
        origin = cv2.imread(image)
        matched = cv2.matchTemplate(fullscreen, origin, cv2.TM_CCOEFF_NORMED)
        _, matched, _, coords = cv2.minMaxLoc(matched)
        if matched > gap:
            print(f"matched {image[-10:]} {matched}/{gap}")
            return tuple[int, int](coords)
        max_val = max(max_val, matched)
    print(f"no matched {max_val}/{gap}")
    return None


def is_full(folder_name: str, gap: float, fullscreen=None) -> bool:
    fullscreen = _read_temp_screen() if fullscreen is not None else _get_cv2_screen()

    gray_fullscreen = cv2.cvtColor(fullscreen, cv2.COLOR_BGR2GRAY)
    examples: list[str] = build_full_paths(folder_name)
    max_val: float = 0
    for image in examples:
        origin = cv2.imread(image)
        gray_origin = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)
        result = ssim(gray_fullscreen, gray_origin)
        if result >= gap:
            print(f"is full. {image[-10:]} {result}/{gap}")
            return True
        max_val = max(max_val, result)
    print(f"no full {max_val}/{gap}")
    return False
