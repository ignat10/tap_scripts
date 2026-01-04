from pathlib import Path
from typing import Callable, Iterator, overload


from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, quality, matchTemplate, minMaxLoc, TM_CCOEFF_NORMED


from ..data.point import Point
from ..data.paths import TEMPLATES_DIR
from .screen_manager import with_screen



def ssim(screen: ndarray, image: ndarray) -> tuple[float, None]:
    """Wrapper for SSIM method."""
    return quality.QualitySSIM_compute(screen, image)[0][0], None


def match_template(screen: ndarray, image: ndarray) -> tuple[float, Point]:
    """Wrapper for cv2.matchTemplate method."""
    matched = matchTemplate(screen, image, TM_CCOEFF_NORMED)
    _, result, _, coords = minMaxLoc(matched)
    return result, Point(tuple(coords))


class Template:
    def __init__(self, relative_path: Path, threshold: float, coords: tuple[int, int] | None = None):
        self.images: dict[str, ndarray] = {}
        self.path = relative_path
        self.threshold = threshold
        self.coords = coords

    def get_images(self) -> Iterator[ndarray]:
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self.images:
                self.images[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self.images[file_name]

    def compare_loop(
            self,
            screen: ndarray,
            compare_method: Callable[[ndarray, ndarray], tuple[float, Point | None]]
            ) -> bool | Point:
            threshold = self.threshold
            for image in self.get_images():
                similarity, coords = compare_method(screen, image)
                if similarity >= threshold:
                    return coords or True
            return False

    def crop_screen(self, screen: ndarray) -> ndarray:
        corner = self.coords
        y, x = self.get_images().__next__().shape
        opposite_corner = (corner[0] + x, corner[1] + y)
        crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
        return crop_screen

    @overload
    def find_part(self, *, do_screen: bool = True) -> bool | Point: ...
    @overload
    def compare_part(self, *, do_screen: bool = True) -> bool: ...
    @overload
    def compare_full(self, *, do_screen: bool = True) -> bool: ...
    
    @with_screen
    def find_part(self, screen: ndarray) -> bool | Point:
        return self.compare_loop(screen, match_template)
    
    @with_screen
    def compare_part(self, screen: ndarray) -> bool:
        cropped_screen = self.crop_screen(screen)
        return self.compare_loop(cropped_screen, ssim)

    @with_screen
    def compare_full(self, screen: ndarray) -> bool:
        return self.compare_loop(screen, ssim)
