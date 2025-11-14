import cv2
from skimage.metrics import structural_similarity as ssim
from numpy import ndarray


from ..utils.loaders import read_images
from .screen_manager import get_screen


images = read_images()


def loop_images(method):
    def wrapper(folder_name: str, gap: float, do_screen=True, **kwargs) -> bool | tuple | None:
        screen = get_screen(do_screen)
        for image in images[folder_name].values():
            result = method(screen, image, gap, **kwargs)
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
    cutted = _cut(screen, image, coords)
    result = ssim(image, cutted, win_size=min(image.shape))
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