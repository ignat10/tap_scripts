from time import sleep
from typing import TypeVar

from ..image_tools import compare_methods, screen_manager
from ..device import actions

from . import point_obj, template_obj


R = TypeVar("R")



class GameObject:
    def __init__(
            self,
            point: dict | None=None,
            template: dict | None=None
    ) -> None:
        self.point: point_obj.Point | None = point_obj.Point(**point) if point is not None else None
        self.template: template_obj.Template | None = template_obj.Template(**template) if template is not None else None

    @point_obj.step
    def click(
        self,
        coords: point_obj.Coords,
        *,
        delay: float = 0.0,
        repeat: int = 1
    ) -> None:
        sleep(delay)
        for _ in range(repeat):
            actions.input_tap(coords)
        screen_manager.reset_temp_screen()

    @screen_manager.with_screen
    def find_and_click(self, screen):
        if coords := self.template.compare_loop(screen, compare_methods.match_template):
            actions.input_tap(coords)
            screen_manager.reset_temp_screen()
            return True
        return False

    @screen_manager.with_screen
    def compare_part(self, screen, steps=0):
        cropped_screen = self.template.crop_screen(screen, steps=steps)
        return self.template.compare_loop(cropped_screen, compare_methods.ssim)

    @point_obj.step
    @screen_manager.with_screen
    def quiq_compare(self, screen, coords):
        cropped_screen = self.template.crop_screen(screen, coords)
        return self.template.compare_loop(cropped_screen, compare_methods.numpy_diff)