from os import path, listdir
from enum import Enum
from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY



class Templates(Enum):
    ADS = "ads"
    BLUE = "blue"
    CITIES = "cities"
    FAVOURITES = "favourites"
    GATHER = "gather"
    LOAD = "load"
    MAIN_MENUS = "main_menus"
    SEARCH_BAR = "search_menus"
    XS = "xs"
    LEO = path.join("avatars", "leo")
    LORD = path.join("avatars", "lord")


THRESHOLDS: dict[Folders, float] = {
    Folders.ADS: 0.9,
    Folders.BLUE: 0.8,
    Folders.CITIES: 0.8,
    Folders.FAVOURITES: 0.8,
    Folders.GATHER: 0.8,
    Folders.LOAD: 0.9,
    Folders.MAIN_MENUS: 0.9,
    Folders.SEARCH_BAR: 0.9,
    Folders.XS: 0.8,

    Folders.LEO: 0.8,
    Folders.LORD: 0.8,
}


_BASE_DIR = path.dirname(path.dirname(__file__))  # packages
_DATA_DIR = path.join(_BASE_DIR, 'data')
_TEMPLATES_DIR = path.join(_DATA_DIR, 'templates')
_LOCAL_DIR = path.join(_BASE_DIR, 'local')
screen_state_path = path.join(_LOCAL_DIR, 'screen.png')
cut_screen = path.join(_LOCAL_DIR, 'cut_screen.png')
farms_sheet_path = path.join(_DATA_DIR, 'WAO_farms_data.xlsx')

folder_names: set[str] = set(listdir(_TEMPLATES_DIR))
folders_enum: set[str] = {item.value for item in Folders}
threshold_names: set[str] = {folder.value for folder in THRESHOLDS}

# assert folder_names == folders_enum, f"expected {folders_enum - folder_names}, found {folder_names - folders_enum}"
# assert folder_names == threshold_names, f"expected {folders_enum - threshold_names}, found {threshold_names - folders_enum}"

folder_paths: dict[Folders, str] = {
    folder: path.join(_TEMPLATES_DIR, folder.value)
    for folder in Folders
}

image_names: dict[Folders, frozenset[str]] = {
    folder: frozenset(listdir(folder_path))
    for folder, folder_path in folder_paths.items()
}

image_paths: dict[Templates, dict[str, str]] = {
    folder: {
        image_name: path.join(folder_path, image_name)
        for image_name in image_names[folder]
    }
    for folder, folder_path in folder_paths.items()
}


images: dict[Templates, dict[str, ndarray]] = {
    folder: {
        image_name: cvtColor(imread(image_path), COLOR_BGR2GRAY)
        for image_name, image_path in image_paths.items()
    }
    for folder, image_paths in image_paths.items()
}


def get_paths(dir: str = _TEMPLATES_DIR):
    return {
        item: 
        get_paths(full)
        if path.isdir((full := path.join(dir, item)))
        else full
        for item in listdir(dir)
    }
p = get_paths()
print(p)