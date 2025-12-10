import cv2
from numpy import ndarray
from enum import Enum, auto


from .screen_manager import get_screen
from .image_manager import Templates



class Status(Enum):
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def ssim(screen: ndarray, image: ndarray) -> float:
    """"Wrapper for SSIM function."""
    from cv2.quality import QualitySSIM_compute
    return QualitySSIM_compute(screen, image)[0][0]


def loop_images(method):
    def wrapper(templates: Templates, do_screen=True) -> bool | tuple:
        template = templates.value
        screen = get_screen(do_screen)
        threshold = template.threshold
        for image in template.get().values():
            similarity, coords = method(screen, image, templates)
            if similarity >= threshold:
                return coords or True
        return False
    return wrapper


@loop_images
def find_part(screen, image, template: Templates) -> tuple[float, tuple[int, int]]:
    matched = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
    _, result, _, coords = cv2.minMaxLoc(matched)
    return result, tuple(coords)


@loop_images
def compare_part(screen, image, template: Templates) -> tuple[float, None]:
    cut = _cut(screen, image, template.value.coords)
    result = ssim(image, cut)
    return result, None


@loop_images
def compare_screen(screen: ndarray, image: ndarray, template: Templates) -> tuple[float, None]:
    return ssim(screen, image), None


def _cut(screen: ndarray, image: ndarray, coords: tuple[int, int]) -> ndarray:
    image_shaped = image.shape
    h, w = image_shaped[:2]
    x_half = w // 2
    y_half = h // 2
    section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
    x0, x1, y0, y1 = section
    crop_screen = screen[y0:y1, x0:x1]
    return crop_screen


def check_status() -> Status:
    if not compare_part(Templates.BOOK):  # book icon position
        return Status.NOT_MAP

    if find_part(Templates.CITIES, do_screen=False):
        return Status.NOT_FOUND

    if find_part(Templates.GATHER, do_screen=False):
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE
