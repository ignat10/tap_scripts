import cv2
from skimage.metrics import structural_similarity as ssim

from my_packages.core.adb_utils import make_screen
from my_packages.data.paths import screen_state_path, build_full_paths



def _read_temp_screen():
    return cv2.imread(screen_state_path)


def _get_cv2_screen():
    make_screen()
    return _read_temp_screen()


def _cut_screen(x0, x1, y0, y1):
    screen = _read_temp_screen()
    cutted = screen[y0:y1, x0:x1]
    return cutted


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


def check_part_screen(folder: str, coords: tuple[int, int], gap: float) -> bool:
    make_screen()
    paths = build_full_paths(folder)
    for image in paths:
        origin = cv2.imread(image)
        shaped = origin.shape
        size = (shaped[1], shaped[0])
        x_half, y_half = size[0] // 2, size[1] // 2
        section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
        cutted = _cut_screen(*section)
        resized = cv2.resize(cutted, size)
        result = ssim(resized, origin, win_size=size[1])
        print(f"ssim result: {result}")
        if result > gap:
            return True
    return False


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
