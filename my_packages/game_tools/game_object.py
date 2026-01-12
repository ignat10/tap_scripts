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
        if coords is not None:
            self.coords: tuple[int, int] = tuple(coords)
        if delta is not None:
            self.delta: tuple[int, Axis] = (delta[0], Axis[delta[1]])
        if path is not None:
            self.path: Path = Path(path)
        if threshold is not None:
            self.threshold = threshold
        self._cache: dict[str, ndarray] = {}

    @property
    def images(self) -> Iterator[ndarray]:
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self._cache:
                self._cache[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self._cache[file_name]

    def _compare_loop(
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

    def _crop_screen(self, screen: ndarray, coords: tuple[int, int]) -> ndarray:
        if coords is None:
            return screen
        corner = coords
        y, x = next(self.images).shape
        opposite_corner = (corner[0] + x, corner[1] + y)
        crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
        return crop_screen

    @staticmethod
    def _step(func):
        def wrapper(self: Self, steps: int=0, *args, **kwargs) -> bool | tuple[int, int]:
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

    @overload
    def click(self, *, delay: float=0.0, steps: int=0, repeat: int=1) -> None: ...
    @overload
    def find_and_click(self, *, do_screen: bool=True, base_object: Self | None = None) -> bool | tuple[int, int]: ...
    @overload
    def compare_part(self, *, do_screen: bool=True, steps: int=0) -> bool: ...

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
    def find_and_click(self, screen: ndarray, base_object: Self) -> None:
        coords = self._compare_loop(screen, compare_methods.match_template) or base_object
        actions.input_tap(coords)

    @_step
    @screen_manager.with_screen
    def compare_part(self, coords, screen: ndarray) -> bool:
        cropped_screen = self._crop_screen(screen, coords)
        return self._compare_loop(cropped_screen, compare_methods.ssim)

    @_step
    def tap(self):
        actions.input_tap([500, 500])
        