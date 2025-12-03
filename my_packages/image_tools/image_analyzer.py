import cv2
from cv2.quality import QualitySSIM_compute as ssim
from numpy import ndarray
from enum import Enum, auto


from .screen_manager import get_screen
from .image_manager import Templates, get_images, THRESHOLDS



class Status(Enum):
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def loop_images(method):
    def wrapper(folder: Templates, do_screen=True, **kwargs) -> bool | tuple | None:
        screen = get_screen(do_screen)
        threshold = THRESHOLDS[folder]
        for image in get_images(folder).values():
            result = method(screen, image, **kwargs)
            match result:
                case float() as similarity if similarity >= threshold:
                    return True
                case (similarity, coords) if similarity >= threshold:
                    return coords
        return None
    return wrapper


@loop_images
def find_part(screen, image) -> tuple[float, tuple]:
    matched = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
    _, result, _, coords = cv2.minMaxLoc(matched)
    return result, tuple(coords)


@loop_images
def compare_part(screen, image, coords: tuple[int, int]) -> float:
    cut = _cut(screen, image, coords)
    result = ssim(image, cut)[0]
    from skimage.metrics import structural_similarity as ssimm
    old = ssimm(image, cut)
    print(f"ssim cv2 result: {result} old structural ssim: {old}")
    return result


@loop_images
def compare_screen(screen: ndarray, image: ndarray) -> float:
    return float(ssim(screen, image))


def _cut(screen: ndarray, image: ndarray, coords: tuple[int, int]) -> ndarray:
    image_shaped = image.shape
    image_size = (image_shaped[1], image_shaped[0])
    x_half = image_size[0] // 2
    y_half = image_size[1] // 2
    section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
    x0, x1, y0, y1 = section
    crop_screen = screen[y0:y1, x0:x1]
    return crop_screen


def check_status() -> Status:
    if not compare_part(Templates.BOOK, coords=(80, 2050)):  # book icon position
        return Status.NOT_MAP

    if not find_part(Templates.CITIES):
        return Status.NOT_FOUND

    if find_part(Templates.GATHER):
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE
