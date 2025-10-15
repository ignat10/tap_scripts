from my_packages.adb_helpers.game_actions import Farm
from my_packages.data.farms import accounts, leo
from my_packages.utils.inputter import farm_number


def make_castles() -> list[Farm]:
    castles: list = []
    number = 1
    for google, count in enumerate(accounts[farm_number()::]):
        for account in range(count):
            castles.append(Farm(number, leo[0], google, account, leo[1], leo[2]))
            number += 1
    return castles


def read_images() -> dict[str, list]:
    from cv2 import imread
    from my_packages.data.paths import path
    images: dict[str, list] = {folder_name: list(imread(image_path) for image_path in image_paths) for folder_name, image_paths in path.image_paths.items()}
    return images
