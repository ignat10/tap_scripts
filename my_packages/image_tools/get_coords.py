from my_packages.image_tools.image_actions import search_part


def x() -> tuple[int, int] | None:
    coords = search_part("xs", 0.9)
    return coords
