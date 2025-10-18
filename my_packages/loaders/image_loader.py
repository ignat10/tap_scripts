from cv2 import imread
from numpy import ndarray

from my_packages.data.paths import path


def read_images() -> dict[str, list[ndarray]]:
    images: dict[str, list] = {folder_name: list(imread(image_path) for image_path in image_paths) for folder_name, image_paths in path.image_paths.items()}
    return images
