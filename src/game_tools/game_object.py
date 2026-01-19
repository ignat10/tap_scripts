from time import sleep
from dataclasses import dataclass, field
from typing import Iterator, Callable, overload, Self
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


class GameObject:
    def __init__(
            self,
            coords: list[int] | None = None,
            delta: list[int | str] | None = None,
            path: str | None = None,
            threshold: float | None = None, 
    ) -> None:
        self.coords: tuple[int, int] | None = (tuple(coords) if coords is not None else None)
        self.delta: tuple[int, Axis] | None = ((delta[0], Axis[delta[1]]) if delta is not None else None)
        self.path: Path | None = (Path(path) if path is not None else None)
        self.threshold: float | None = (float(threshold) if threshold is not None else None)
        self._cache: dict[str, ndarray] = {}

    @staticmethod
    def _step(func):
        def wrapper(self: Self, steps: int=0, *args, **kwargs) -> bool | tuple[int, int]:
            assert self.coords is not None, f"try to make step for {self.path} without coords"
            if steps == 0:
                moved_coords = self.coords
            else:
                offset = self.delta[0]
                axis = self.delta[1]
                lst = list(self.coords)

                lst[axis.value] += offset * steps
                moved_coords = tuple(lst)
            return func(self, coords=moved_coords, *args, **kwargs)
        return wrapper
    
    @property
    def images(self) -> Iterator[ndarray]:
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self._cache:
                self._cache[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self._cache[file_name]

    @overload
    def _compare_loop(self, screen: ndarray, compare_method: Callable[[ndarray, ndarray], tuple[float, None]]) -> bool: ...
    @overload
    def _compare_loop(self, screen: ndarray, compare_method: Callable[[ndarray, ndarray], tuple[float, tuple[int, int]]]) -> tuple[int, int] | None: ...
    @overload
    def click(self, *, delay: float=0.0, steps: int=0, repeat: int=1) -> None: ...
    @overload
    def find_and_click(self, *, do_screen: bool=True) -> bool: ...
    @overload
    def compare_part(self, *, do_screen: bool=True, steps: int=0) -> bool: ...

    def _compare_loop(self, screen, compare_method):
        threshold = self.threshold
        for image in self.images:
            similarity, coords = compare_method(screen, image)
            if similarity >= threshold:
                return coords or True
        return None

    def _crop_screen(self, screen: ndarray, coords: tuple[int, int]) -> ndarray:
        if coords is None:
            return screen
        corner = coords
        y, x = next(self.images).shape
        opposite_corner = (corner[0] + x, corner[1] + y)
        crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
        return crop_screen

    @_step
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
    def find_and_click(self, screen):
        if coords := self._compare_loop(screen, compare_methods.match_template):
            actions.input_tap(coords)
            return True
        return False
    
    @screen_manager.with_screen
    @_step
    def compare_part(self, screen, coords):
        cropped_screen = self._crop_screen(screen, coords=coords)
        return self._compare_loop(cropped_screen, compare_methods.ssim)
