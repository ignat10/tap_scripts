from my_packages.data.paths import path
from my_packages.image_tools.image_actions import search_part


def x():
    coords = search_part(path["xs"], 0.9)
    return coords
