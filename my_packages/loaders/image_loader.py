from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from numpy import ndarray

from my_packages.data.paths import path


def read_images() -> dict[str, list[ndarray]]:
    images: dict[str, list] = {folder_name: list(cvtColor(imread(image_path), COLOR_BGR2GRAY) for image_path in image_paths) for folder_name, image_paths in path.image_paths.items()}
    return images
