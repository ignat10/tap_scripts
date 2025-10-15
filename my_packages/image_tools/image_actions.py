import cv2
from skimage.metrics import structural_similarity as ssim

from my_packages.core.adb_utils import make_screen
from my_packages.data.paths import path
from my_packages.utils.setup import read_images


images = read_images()


def _read_temp_screen():
    return cv2.imread(path.screen_state_path)


def _get_cv2_screen():
    make_screen()
    return _read_temp_screen()


def _cut_screen(x0, x1, y0, y1):
    screen = _read_temp_screen()
    cutted = screen[y0:y1, x0:x1]
    return cutted


def search_part(folder_name: str, gap: float, fullscreen=None) -> tuple | None:
    fullscreen = _read_temp_screen() if fullscreen is not None else _get_cv2_screen()

    max_val: float = 0.0
    for origin in images[folder_name]:
        matched = cv2.matchTemplate(fullscreen, origin, cv2.TM_CCOEFF_NORMED)
        _, matched, _, coords = cv2.minMaxLoc(matched)
        if matched > gap:
            print(f"matched {matched}/{gap}")
            return tuple(coords)
        max_val = max(max_val, matched)
    print(f"no matched {max_val}/{gap}")
    return None


def check_part_screen(folder: str, coords: tuple[int, int], gap: float) -> bool:
    make_screen()
    for image in images[folder]:
        shaped = image.shape
        size = (shaped[1], shaped[0])
        x_half, y_half = size[0] // 2, size[1] // 2
        section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
        cutted = _cut_screen(*section)
        resized = cv2.resize(cutted, size)
        result = ssim(resized, image, win_size=size[1])
        print(f"ssim result: {result}")
        if result > gap:
            return True
    return False


def is_full(folder_name: str, gap: float, fullscreen=None) -> bool:
    fullscreen = _read_temp_screen() if fullscreen is not None else _get_cv2_screen()

    gray_fullscreen = cv2.cvtColor(fullscreen, cv2.COLOR_BGR2GRAY)
    max_val: float = 0
    for image in images[folder_name]:
        gray_origin = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = ssim(gray_fullscreen, gray_origin)
        if result >= gap:
            print(f"is full. {result}/{gap}")
            return True
        max_val = max(max_val, result)
    print(f"no full {max_val}/{gap}")
    return False
