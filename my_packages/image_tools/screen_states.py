from enum import Enum

from my_packages.image_tools.image_actions import ImageAnalyzer


class Mine(Enum):
    NOT_MAP = 0
    NOT_FOUND = 1
    FOUND_VISIBLE = 2
    FOUND_NOT_VISIBLE = 3


class ScreenState:
    def __init__(self):
        self.image_analyzer = ImageAnalyzer()

    def loading(self) -> bool:
        gap = 0.6
        folder = "ads"
        return not self.image_analyzer.match_screen(folder, gap)
    
    def main_menu(self, gap=0.8) -> bool:
        folder = "main_menus"
        return self.image_analyzer.match_screen(folder, gap)
    
    def is_city(self) -> bool:
        gap = 0.6
        folder_name = "cities"
        result = self.image_analyzer.find_part(folder_name, gap, True)
        return bool(result)

    def is_menu(self) -> bool:
        folder_name = "search_menus"
        gap = 0.9
        result = self.image_analyzer.find_part(folder_name, gap)
        return bool(result)
    
    def search_state(self) -> Mine:
        if not self.is_menu():
            return Mine.NOT_MAP

        elif self.is_city():
            return Mine.NOT_FOUND

        elif self.is_visible_gather():
            return Mine.FOUND_VISIBLE

        else:
            return Mine.FOUND_NOT_VISIBLE

    def is_visible_gather(self) -> bool:
        folder_name = "gather"
        gap = 0.6
        result = self.image_analyzer.find_part(folder_name, gap, False)
        return bool(result)

    def is_blue(self, coords: tuple[int, int]) -> bool:
        folder_name = "blue"
        gap = 0.8
        return self.image_analyzer.compare_part(folder_name, coords, gap)

    def get_coords(self) -> tuple[int, int] | None:
        folder_name = "xs"
        gap = 0.9
        coords = self.image_analyzer.find_part(folder_name, gap, False)
        return coords

    def is_avatar(self, castle_name: str):
        gap = 0.8
        return self.image_analyzer.find_part(castle_name, gap)


screen_state = ScreenState()