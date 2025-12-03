from os import path, listdir
from enum import Enum
from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY


_BASE_DIR = path.dirname(path.dirname(__file__))  # packages
_DATA_DIR = path.join(_BASE_DIR, 'data')
_TEMPLATES_DIR = path.join(_DATA_DIR, 'templates')
_LOCAL_DIR = path.join(_BASE_DIR, 'local')
screen_state_path = path.join(_LOCAL_DIR, 'screen.png')
cut_screen = path.join(_LOCAL_DIR, 'cut_screen.png')
farms_sheet_path = path.join(_DATA_DIR, 'WAO_farms_data.xlsx')



class Templates(Enum):
    ADS = "ads"
    BLUE = "blue"
    BOOK = "book"
    CITIES = "cities"
    FAVOURITES = "favourites"
    GATHER = "gather"
    LOAD = "load"
    MAIN_MENUS = "main_menus"
    SEARCH_BAR = "search_menus"
    XS = "xs"

    LEO = path.join("avatars", "leo")
    LORD = path.join("avatars", "lord")

    def __call__(self) -> str:
        return path.join(_TEMPLATES_DIR, self.value)


THRESHOLDS: dict[Templates, float] = {
    Templates.ADS: 0.9,
    Templates.BLUE: 0.8,
    Templates.BOOK: 0.8,
    Templates.CITIES: 0.8,
    Templates.FAVOURITES: 0.8,
    Templates.GATHER: 0.8,
    Templates.LOAD: 0.9,
    Templates.MAIN_MENUS: 0.9,
    Templates.SEARCH_BAR: 0.9,
    Templates.XS: 0.8,

    Templates.LEO: 0.8,
    Templates.LORD: 0.8,
}

def get_paths(local_path: str = "") -> set[str] | None:
    full_path = path.join(_TEMPLATES_DIR, local_path)
    tree = set()

    for item in listdir(full_path):
        item_path = path.join(full_path, item)

        if path.isfile(item_path):
            return None
        tree.update(st if (st := get_paths(path.join(local_path, item))) is not None else {path.join(local_path, item)})

    return tree
    


folder_names: set[str] = get_paths()
Templates_enum: set[str] = {item.value for item in Templates}
threshold_names: set[str] = {folder.value for folder in THRESHOLDS}

assert folder_names == Templates_enum, f"expected {Templates_enum - folder_names}, found {folder_names - Templates_enum}"
assert folder_names == threshold_names, f"expected {Templates_enum - threshold_names}, found {threshold_names - Templates_enum}"


images: dict[Templates, dict[str, ndarray]] = {}

def get_images(template: Templates) -> dict[str, ndarray]:
    global images
    if template not in images:
        templates_path = path.join(_TEMPLATES_DIR, template.value)

        images[template] = {
            file_name: cvtColor(imread(path.join(templates_path, file_name)), COLOR_BGR2GRAY)
            for file_name in listdir(templates_path)
        }

    return images[template]
