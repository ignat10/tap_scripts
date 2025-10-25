import cv2
from numpy import ndarray, frombuffer, uint8
from skimage.metrics import structural_similarity as ssim

from my_packages.core.adb_device import device
from my_packages.loaders.image_loader import read_images


images = read_images()


def _transform_image2np(console_output: str) -> ndarray:
    image_bytes = frombuffer(console_output, uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


def _read_temp_screen():
    return cv2.imread(path.screen_state_path)


def _get_cv2_screen() -> ndarray:
    gray_image = _transform_image2np(screencap())
    return gray_image


def _cut_screen(fullscreen: ndarray, x0, x1, y0, y1) -> ndarray:
    cutted = fullscreen[y0:y1, x0:x1]
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
    gray_fullscreen = _transform_image2np(screencap())
    for origin in images[folder]:
        origin_shaped = origin.shape
        origin_size = (origin_shaped[1], origin_shaped[0])
        x_half, y_half = origin_size[0] // 2, origin_size[1] // 2
        section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)

        cutted = _cut_screen(gray_fullscreen, *section)
        print(f"size of: origin: {origin_size} cutted: {cutted.shape}")
        resized_screen = cv2.resize(cutted, origin_size)
        result = ssim(origin, resized_screen, win_size=min(origin_size))
        print(f"ssim result: {result}")
        if result > gap:
            return True
    return False


def is_full(folder_name: str, gap: float, fullscreen=None) -> bool:
    gray_fullscreen = _read_temp_screen() if fullscreen is not None else _get_cv2_screen()

    max_val: float = 0
    for image in images[folder_name]:
        result = ssim(gray_fullscreen, image)
        if result >= gap:
            print(f"is full. {result}/{gap}")
            return True
        max_val = max(max_val, result)
    print(f"no full {max_val}/{gap}")
    return False
