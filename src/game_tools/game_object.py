from dataclasses import dataclass
from time import sleep
from typing import Iterator, Callable, overload, TypeVar
from enum import Enum
from pathlib import Path

from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY

from ..paths import TEMPLATES_DIR
from ..image_tools import compare_methods, screen_manager
from ..device import actions



R = TypeVar("R")


class Axis(Enum):
    X = 0
    Y = 1

@dataclass(frozen=True)
class Coords:
    x: int
    y: int

@dataclass(frozen=True)
class Delta:
    interval: int
    axis: Axis

class Point:
    def __init__(
            self,
            coords: dict[str, int],
            delta: dict[str, int | str] | None = None
            ) -> None:
        self.coords: Coords = Coords(**coords)
        self.delta: Delta | None = Delta(**delta) if delta is not None else None

class Template:
    def __init__(
            self,
            path: str,
            threshold: float
        ) -> None:
        self.path: Path = Path(path)
        self.threshold: float = threshold

def _step(
    func: Callable[..., R]
    ) -> Callable[..., R]:
    def wrapper(self: "GameObject", *args, steps: int=0, **kwargs) -> R:
        if self.point.delta is None and steps != 0:
            raise ValueError(f"Object {self} has no delta.")
        if steps == 0:
            moved_coords = self.point.coords
        else:
            offset = self.point.delta.interval
            axis = self.point.delta.axis
            lst = list(self.point.coords)

            lst[axis.value] += offset * steps
            moved_coords = tuple(lst)
        return func(self, *args, coords=moved_coords, **kwargs)
    return wrapper
    

class GameObject:
    def __init__(
            self,
            point=None,
            template=None
    ) -> None:
        self.point: Point | None = Point(**point) if point is not None else None
        self.template: Template | None = Template(**template) if template is not None else None
        self._cache: dict[str, ndarray] = {}

    @property
    def images(self) -> Iterator[ndarray]:
        for file_path in (TEMPLATES_DIR / self.template.path).iterdir():
            file_name = file_path.name
            if file_name not in self._cache:
                self._cache[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self._cache[file_name]

    @overload
    def _compare_loop(self, screen: ndarray, compare_method: Callable[[ndarray, ndarray], tuple[float, None]]) -> bool: ...
    @overload
    def _compare_loop(self, screen: ndarray, compare_method: Callable[[ndarray, ndarray], tuple[float, tuple[int, int]]]) -> tuple[int, int] | None: ...
    @overload
    def _crop_screen(self, screen: ndarray, steps: int) -> ndarray: ...
    @overload
    def click(self, *, delay: float=0.0, steps: int=0, repeat: int=1) -> None: ...
    @overload
    def find_and_click(self) -> bool: ...
    @overload
    def compare_part(self, *, steps: int=0) -> bool: ...

    def _compare_loop(self, screen, compare_method):
        if self.template is None:
            raise ValueError(f"Object {self} has no template.")
        
        threshold = self.template.threshold
        for image in self.images:
            similarity, coords = compare_method(screen, image)
            if similarity >= threshold:
                return coords or True
        return None

    @_step
    def _crop_screen(self, screen, coords: Coords) -> ndarray:
        y, x = next(self.images).shape
        opposite_corner = Coords(coords.x + x, coords.y + y)
        crop_screen = screen[coords.y:opposite_corner.y, coords.x:opposite_corner.x]
        return crop_screen

    @_step
    def click(
        self,
        coords: Coords,
        *,
        delay: float = 0.0,
        repeat: int = 1
    ) -> None:
        sleep(delay)
        for _ in range(repeat):
            actions.input_tap(coords.x, coords.y)
        screen_manager.reset_temp_screen()

    @screen_manager.with_screen
    def find_and_click(self, screen):
        if coords := self._compare_loop(screen, compare_methods.match_template):
            actions.input_tap(coords)
            screen_manager.reset_temp_screen()
            return True
        return False

    @screen_manager.with_screen
    def compare_part(self, screen, steps=0):
        cropped_screen = self._crop_screen(screen, steps=steps)
        return self._compare_loop(cropped_screen, compare_methods.ssim)
