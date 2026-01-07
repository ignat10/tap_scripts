from time import sleep
from enum import Enum
from pathlib import Path
from typing import Iterator, Callable, overload


from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, matchTemplate, minMaxLoc, TM_CCOEFF_NORMED, quality


from ..device.actions import input_tap
from ..image_tools.screen_manager import with_screen
from ..data.paths import TEMPLATES_DIR



class Axis(Enum):
    X = 0
    Y = 1


class GameObject:
    def __init__(
        self,
        coords: tuple[int, int] | None = None,
        delta: int | None = None,
        axis: Axis | None = None,
        path: Path | None = None,
        threshold: float | None = None,
    ) -> None:
        self.coords = coords
        self.delta = delta
        self.axis = axis
        self.path = path
        self.threshold = threshold
        self.images: dict[str, ndarray] = {}

    def step(self, steps: int) -> tuple[int, int]:
        if self.coords is None or self.delta is None:
            raise ValueError("Coordinates or delta not defined for this GameObject.")
        
        if steps == 0:
            return self.coords

        lst = list(self.coords)
        lst[self.axis.value] += self.delta * steps
        return tuple(lst)

    def click(
        self,
        delay: float = 0.0,
        steps: int = 0,
        repeat: int = 1
    ) -> None:
        coords = self.step(steps)
        sleep(delay)
        for _ in range(repeat):
            input_tap(coords)

    def get_images(self) -> Iterator[ndarray]:
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self.images:
                self.images[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self.images[file_name]

    def compare_loop(
            self,
            screen: ndarray,
            compare_method: Callable[[ndarray, ndarray], tuple[float, tuple[int, int] | None]]
            ) -> bool | tuple[int, int]:
            threshold = self.threshold
            for image in self.get_images():
                similarity, coords = compare_method(screen, image)
                if similarity >= threshold:
                    return coords or True
            return False

    def crop_screen(self, screen: ndarray) -> ndarray:
        if self.coords is None:
            return screen
        corner = self.coords
        y, x = self.get_images().__next__().shape
        opposite_corner = (corner[0] + x, corner[1] + y)
        crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
        return crop_screen

    @overload
    def find_part(self, *, do_screen: bool = True) -> bool | tuple[int, int]: ...
    @overload
    def compare_part(self, *, do_screen: bool = True) -> bool: ...

    @with_screen
    def find_part(self, screen: ndarray) -> bool | tuple[int, int]:
        def match_template(screen: ndarray, image: ndarray):
            """Wrapper for cv2.matchTemplate method."""
            matched = matchTemplate(screen, image, TM_CCOEFF_NORMED)
            _, result, _, coords = minMaxLoc(matched)
            return result, tuple(coords)    
        return self.compare_loop(screen, match_template)
    
    @with_screen
    def compare_part(self, screen: ndarray) -> bool:
        def ssim(screen: ndarray, image: ndarray) -> tuple[float, None]:
            """Wrapper for SSIM method."""
            return quality.QualitySSIM_compute(screen, image)[0][0], None
        cropped_screen = self.crop_screen(screen)
        return self.compare_loop(cropped_screen, ssim)
