import os.path

from numpy import ndarray


_BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # packages
_SCREENS_DIR = os.path.join(_BASE_DIR, 'image_tools', 'screens')
_DATA_DIR = os.path.join(_BASE_DIR, 'data')
_LOCAL_DIR = os.path.join(_BASE_DIR, 'local')
screen_state_path = os.path.join(_LOCAL_DIR, 'screen.png')
cutted_screen = os.path.join(_LOCAL_DIR, 'cutted_screen.png')
farms_sheet_path = os.path.join(_DATA_DIR, 'WAO_farms_data.xlsx')

folder_names: frozenset[str] = frozenset(os.listdir(_SCREENS_DIR))

folder_paths: dict[str, str] = {
    folder_name: os.path.join(_SCREENS_DIR, folder_name)
    for folder_name in folder_names
}

image_names: dict[str, frozenset[str]] = {
    folder_name: frozenset(os.listdir(folder_path))
    for folder_name, folder_path in folder_paths.items()
}

image_paths: dict[str, dict[str, str]] = {
    folder_name: {
        image_name: os.path.join(folder_path, image_name)
        for image_name in image_names[folder_name]
    }
    for folder_name, folder_path in folder_paths.items()
}


def read_images() -> dict[str, dict[str, ndarray]]:
    from cv2 import imread, cvtColor, COLOR_BGR2GRAY

    return {
        folder_name: {
            image_name: cvtColor(imread(image_path), COLOR_BGR2GRAY)
            for image_name, image_path in image_paths.items()
        }
        for folder_name, image_paths in image_paths.items()
    }


def get_image_gaps() -> dict[str, float]:
    gaps: dict[str, float] = {
        folder_name: 0.9
        for folder_name in folder_names
    }
    gaps.update({
        "ads": 0.6,
        "blue": 0.8,
        "cities": 0.6,
        "gather": 0.6,
        "main_menus": 0.8,
    })
    return gaps
