from enum import Enum
from pathlib import Path


from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY


from ..data.paths import TEMPLATES_DIR



class Template:
    def __init__(self, relative_path: str, threshold: float, coords: tuple[int, int] | None = None):
        self.images = None
        self.path = relative_path
        self.threshold = threshold
        self.coords = coords

    def get(self):
        if self.images is None:
            self.images: dict[str, ndarray] = {
                file_path: cvtColor(imread(file_path), COLOR_BGR2GRAY)
                for file_path in (TEMPLATES_DIR / self.path).iterdir()
            }
        return self.images
    

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
