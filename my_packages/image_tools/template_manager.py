from enum import Enum, auto
from pathlib import Path
from typing import Callable


from numpy import ndarray
import cv2

from ..data.poco_coordinates import Point
from ..data.paths import TEMPLATES_DIR
from .screen_manager import get_screen



def ssim(screen: ndarray, image: ndarray) -> float:
    """"Wrapper for SSIM function."""
    return cv2.quality.QualitySSIM_compute(screen, image)[0][0], None


def match_template(screen: ndarray, image: ndarray) -> float:
    """Wrapper for cv2.matchTemplate function."""
    matched = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
    _, result, _, coords = cv2.minMaxLoc(matched)
    return result, Point(coords)


def compare_loop(compare_method: Callable[[ndarray], tuple[ndarray, Callable[[ndarray, ndarray], tuple[float, Point | None]]]]):
    def wrapper(self: Template, do_screen=True) -> bool | Point:
        screen, method = compare_method(get_screen(do_screen))
        templates = self.get_images()
        threshold = self.threshold
        for image in templates.values():
            similarity, coords = method(screen, image)
            if similarity >= threshold:
                return coords or True
        return False
    return wrapper


class Template:
    def __init__(self, relative_path: Path, threshold: float, coords: tuple[int, int] | None = None):
        self.images = None
        self.path = relative_path
        self.threshold = threshold
        self.coords = coords

    def get_images(self):
        if self.images is None:
            self.images: dict[str, ndarray] = {
                file_path.name: cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2GRAY)
                for file_path in (TEMPLATES_DIR / self.path).iterdir()
            }
        return self.images
    
    def crop_screen(self, screen: ndarray) -> ndarray:
        corner = self.coords
        y, x = next(self.get_images().values()).shape
        opposite_corner = (corner[0] + x, corner[1] + y)
        crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
        return crop_screen
    
    @compare_loop
    @staticmethod
    def find_part(screen: ndarray) -> tuple[ndarray, function]:
        return screen, match_template

    @compare_loop
    def compare_part(self,screen: ndarray) -> tuple[ndarray, function]:
        cropped_screen = self.crop_screen(screen)
        return cropped_screen, ssim
    
    @compare_loop
    @staticmethod
    def compare_full(screen: ndarray) -> tuple[ndarray, function]:
        return screen, ssim

    

class Templates(Enum):
    ADS = Template(Path("ads"), 0.9)
    BLUE = Template(Path("blue"), 0.8)
    BOOK = Template(Path("book"), 0.8, coords=(88, 2069))
    CITIES = Template(Path("cities"), 0.8)
    FAVOURITES = Template(Path("favourites"), 0.8)
    GATHER = Template(Path("gather"), 0.8)
    LOAD = Template(Path("load"), 0.9)
    MAIN_MENUS = Template(Path("main_menus"), 0.9)
    SEARCH_BAR = Template(Path("search_menus"), 0.9)
    XS = Template(Path("xs"), 0.8)
    LEO = Template(Path("avatars/leo"), 0.8)
    LORD = Template(Path("avatars/lord"), 0.8)
    MINE = Template(Path("mines"), 0.8, coords=(614, 1324))


class Status(Enum):
    NOT_MAP = auto()
    NOT_FOUND = auto()
    FOUND_VISIBLE = auto()
    FOUND_NOT_VISIBLE = auto()


def check_status() -> Status:
    if not Templates.BOOK.value.compare_part():
        return Status.NOT_MAP

    if Templates.CITIES.value.find_part(do_screen=False):
        return Status.NOT_FOUND

    if Templates.GATHER.value.find_part(do_screen=False):
        return Status.FOUND_VISIBLE

    else:
        return Status.FOUND_NOT_VISIBLE
