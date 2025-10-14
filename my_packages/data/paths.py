import os.path

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) # packages
SCREENS_DIR = os.path.join(BASE_DIR, 'image_tools', 'screens')
screen_state_path = os.path.join(BASE_DIR, 'local', 'screen.png')



def build_image_paths() -> dict[str, list[str]]:
    result = {}
    for folder in os.listdir(SCREENS_DIR):
        result[folder] = []
        for image in os.listdir(os.path.join(SCREENS_DIR, folder)):
            result[folder].append(image)
    return result


def build_full_paths(key: str) -> list[str]:
    result = []
    for image in _path[key]:
        full_path = os.path.join(SCREENS_DIR, key, image)
        result.append(full_path)
    return result


_path = build_image_paths()
print(_path)
