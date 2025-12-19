from os import path, listdir
from enum import Enum
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
                file_name: cvtColor(imread(path.join(TEMPLATES_DIR, self.path, file_name)), COLOR_BGR2GRAY)
                for file_name in listdir(path.join(TEMPLATES_DIR, self.path))
            }
        return self.images
    

class Templates(Enum):
    ADS = Template("ads", 0.9)
    BLUE = Template("blue", 0.8)
    BOOK = Template("book", 0.8, coords=(88, 2069))
    CITIES = Template("cities", 0.8)
    FAVOURITES = Template("favourites", 0.8)
    GATHER = Template("gather", 0.8)
    LOAD = Template("load", 0.9)
    MAIN_MENUS = Template("main_menus", 0.9)
    SEARCH_BAR = Template("search_menus", 0.9)
    XS = Template("xs", 0.8)
    LEO = Template("avatars/leo", 0.8)
    LORD = Template("avatars/lord", 0.8)
    MINE = Template("mines", 0.8, coords=(614, 1324))


def get_paths(local_path: str = "") -> set[str]:
    full_path = path.join(TEMPLATES_DIR, local_path)
    tree = set()

    for item in listdir(full_path):
        item_path = path.join(full_path, item)

        if path.isfile(item_path):
            return None
        tree.update(st if (st := get_paths(path.join(local_path, item))) is not None else {path.join(local_path, item)})

    return tree
    

listdir_paths: set[str] = get_paths()
Templates_enum: set[str] = {item.value.path for item in Templates}

assert listdir_paths == Templates_enum, f"expected {Templates_enum - listdir_paths}, found {listdir_paths - Templates_enum}"
