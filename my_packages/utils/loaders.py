from numpy import ndarray

def read_images() -> dict[str, dict[str, ndarray]]:
    from cv2 import imread, cvtColor, COLOR_BGR2GRAY
    from ..data.paths import path
    return {
        folder_name: {
            image_name: cvtColor(imread(image_path), COLOR_BGR2GRAY)
            for image_name, image_path in image_paths.items()
        }
        for folder_name, image_paths in path.image_paths.items()
    }



from ..game_tools.actions import Farm

def make_castles() -> list[Farm]:
    from ..data.farms import farms_sheet
    from .inputter import farm_number
    castles: list = []
    for row in farms_sheet.values[farm_number()::]:
        castles.append(Farm(*row))
    return castles
