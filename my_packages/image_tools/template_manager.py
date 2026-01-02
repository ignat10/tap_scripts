from enum import Enum, auto
from pathlib import Path
from typing import Callable, Self


from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, quality, matchTemplate, minMaxLoc, TM_CCOEFF_NORMED

from ..data.poco_coordinates import Point
from ..data.paths import TEMPLATES_DIR
from .screen_manager import get_screen



def ssim(screen: ndarray, image: ndarray) -> tuple[float, None]:
    """"Wrapper for SSIM function."""
    return quality.QualitySSIM_compute(screen, image)[0][0], None


def match_template(screen: ndarray, image: ndarray) -> tuple[float, Point]:
    """Wrapper for cv2.matchTemplate function."""
    matched = matchTemplate(screen, image, TM_CCOEFF_NORMED)
    _, result, _, coords = minMaxLoc(matched)
    return result, Point(tuple(coords))


class Template:
    def __init__(self, relative_path: Path, threshold: float, coords: tuple[int, int] | None = None):
        self.images: dict[str, ndarray] = {}
        self.path = relative_path
        self.threshold = threshold
        self.coords = coords

    def get_images(self):
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self.images:
                self.images[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self.images[file_name]

    def compare_loop(self, compare_method: Callable[[ndarray, ndarray], tuple[tuple[float, Point | None]]]):
        def wrapper(self, ) -> bool | Point:
            screen, method = compare_method(self, get_screen(do_screen))
            threshold = self.threshold
            for image in self.get_images():
                similarity, coords = method(screen, image)
                if similarity >= threshold:
                    return coords or True
            return False
        return wrapper
    
    def crop_screen(self, screen: ndarray) -> ndarray:
        corner = self.coords
        y, x = self.get_images().values().__iter__().__next__().shape
        opposite_corner = (corner[0] + x, corner[1] + y)
        crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
        return crop_screen

    @compare_loop
    def find_part(self, screen: ndarray) -> tuple[ndarray, Callable[[ndarray, ndarray], tuple[float, Point]]]:
        return screen, match_template

    @compare_loop
    def compare_part(self, screen: ndarray) -> tuple[ndarray, Callable[[ndarray, ndarray], tuple[float, None]]]:
        cropped_screen = self.crop_screen(screen)
        return cropped_screen, ssim
    
    @compare_loop
    def compare_full(self, screen: ndarray) -> tuple[ndarray, Callable[[ndarray, ndarray], tuple[float, None]]]:
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
