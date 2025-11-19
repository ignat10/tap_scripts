import cv2
from skimage.metrics import structural_similarity as ssim
from numpy import ndarray
from enum import Enum


from .screen_manager import get_screen
from .image_manager import read_images, get_image_gaps

images = read_images()
gaps = get_image_gaps()


class Status(Enum):
    NOT_MAP = 0
    NOT_FOUND = 1
    FOUND_VISIBLE = 2
    FOUND_NOT_VISIBLE = 3



def loop_images(method):
    def wrapper(folder_name: str, do_screen=True, **kwargs) -> bool | tuple | None:
        screen = get_screen(do_screen)
        gap = gaps[folder_name]
        for image in images[folder_name].values():
            result = method(screen, image, **kwargs)
            match result:
                case float() as similarity if similarity >= gap:
                    return True
                case (similarity, coords) if similarity >= gap:
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
    result = ssim(image, cut, win_size=min(image.shape))
    return result


@loop_images
def match_screen(screen: ndarray, image: ndarray) -> float:
    return float(ssim(screen, image))


def _cut(screen: ndarray, image: ndarray, coords: tuple[int, int]) -> ndarray:
    image_shaped = image.shape
    image_size = (image_shaped[1], image_shaped[0])
    x_half, y_half = image_size[0] // 2, image_size[1] // 2
    section = (coords[0] - x_half, coords[0] + x_half, coords[1] - y_half, coords[1] + y_half)
    x0, x1, y0, y1 = section
    print(f"section: {x1 - x0, y1 - y0}, shape: {image_size} should be same")
    return screen[y0:y1, x0:x1]


def check_status() -> Status:
    if not find_part("map"):
        return Status.NOT_MAP

    if not find_part("cities"):
        return Status.NOT_FOUND

    if find_part("gather"):
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE