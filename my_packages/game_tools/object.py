from time import sleep
from dataclasses import dataclass, field
from typing import Iterator, Callable, overload
from enum import Enum
from pathlib import Path


from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY


from ..data.paths import TEMPLATES_DIR
from ..image_tools import compare_methods, screen_manager
from ..device import actions



class Axis(Enum):
    X = 0
    Y = 1


def step(func):
    def wrapper(self, steps: int=0, *args, **kwargs) -> bool | tuple[int, int]:
        if steps == 0:
            return self.coords
        
        offset = self.delta[0]
        axis = self.delta[1]
        lst = list(self.coords)

        lst[axis.value] += offset * steps
        return func(self, tuple(lst), *args, **kwargs)
    return wrapper


@dataclass
class GameObject:
    coords: tuple[int, int] | None = None
    delta: tuple[int, Axis] | None = None
    path: str | None = None
    threshold: float | None = None
    _cache: dict[str, ndarray] = field(default_factory=dict)

    def __post_init__(self):
        if self.path is not None:
            self.path = Path(self.path)

    @property
    def images(self) -> Iterator[ndarray]:
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self._cache:
                self._cache[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self._cache[file_name]

    def compare_loop(
            self,
            screen: ndarray,
            compare_method: Callable[[ndarray, ndarray], tuple[float, tuple[int, int] | None]]
            ) -> bool | tuple[int, int]:
            threshold = self.threshold
            for image in self.images:
                similarity, coords = compare_method(screen, image)
                if similarity >= threshold:
                    return coords or True
            return False

    def crop_screen(self, screen: ndarray, coords: tuple[int, int]) -> ndarray:
        if coords is None:
            return screen
        corner = coords
        y, x = next(self.images).shape
        opposite_corner = (corner[0] + x, corner[1] + y)
        crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
        return crop_screen

    @overload
    def click(self, *, delay: float=0.0, steps: int=0, repeat: int=1) -> None: ...
    @overload
    def find_part(self, *, do_screen: bool=True) -> bool | tuple[int, int]: ...
    @overload
    def compare_part(self, *, do_screen: bool=True, steps: int=0) -> bool: ...

    @step
    def click(
        self,
        coords: tuple[int, int],
        delay: float = 0.0,
        repeat: int = 1
    ) -> None:
        sleep(delay)
        for _ in range(repeat):
            actions.input_tap(coords)

    @screen_manager.with_screen
    def find_and_click(self, screen) -> None:
        coords = self.templates.compare_loop(screen, compare_methods.match_template)
        if isinstance(coords, tuple):
            actions.input_tap(coords)

    @step
    @screen_manager.with_screen
    def compare_part(self, coords, screen) -> bool:
        cropped_screen = self.templates.crop_screen(screen, coords)
        return self.templates.compare_loop(cropped_screen, compare_methods.ssim)
