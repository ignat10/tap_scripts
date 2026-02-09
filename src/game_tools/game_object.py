from dataclasses import dataclass
from time import sleep
from typing import Iterator, Callable, Literal, TypeVar
from pathlib import Path

from numpy import ndarray
from cv2 import imread, cvtColor, COLOR_BGR2GRAY

from ..paths import TEMPLATES_DIR
from ..image_tools import compare_methods, screen_manager
from ..device import actions



R = TypeVar("R")



@dataclass(frozen=True)
class Coords:
    x: int
    y: int

@dataclass(frozen=True)
class Delta:
    interval: int
    axis: Literal["x", "y"]

@dataclass
class Point:
    coords: dict[str, int]
    delta: dict[str, int | str] | None = None
    def __post_init__(
        self,
    ) -> None:
        self.coords: Coords = Coords(**self.coords)
        self.delta: Delta | None = Delta(**self.delta) if self.delta is not None else None

def step(
    func: Callable[..., R]
    ) -> Callable[..., R]:
    def wrapper(self: "GameObject", *args, steps: int=0, **kwargs) -> R:
        if steps == 0:
            moved_coords = self.point.coords
        elif self.point.delta is None:
            raise ValueError(f"Object {self} has no delta.")
        else:
            delta = self.point.delta * steps
            x, y = self.point.coords.x, self.point.coords.y
            
            match self.point.delta.axis:
                case "x":
                    moved_coords = Coords(x + delta, y)
                case "y":
                    moved_coords = Coords(x, y + delta)
                
        return func(self, *args, coords=moved_coords, **kwargs)
    return wrapper


class Template:
    def __init__(
            self,
            path: str,
            threshold: float
        ) -> None:
        self.path: Path = Path(path)
        self.threshold: float = threshold
        self._cache: dict[str, ndarray] = {}

    @property
    def images(self) -> Iterator[ndarray]:
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self._cache:
                self._cache[file_name] = cvtColor(imread(file_path), COLOR_BGR2GRAY)
            yield self._cache[file_name]

    @step
    def crop_screen(self, screen: ndarray, coords: Coords) -> ndarray:
        y, x = next(self.images).shape
        opposite_corner = Coords(coords.x + x, coords.y + y)
        crop_screen = screen[coords.y:opposite_corner.y, coords.x:opposite_corner.x]
        return crop_screen

    def compare_loop(self, screen, compare_method: Callable[[ndarray, ndarray, float], R]) -> R:
        threshold = self.threshold
        result: R | None = None
        for image in self.images:
            result = compare_method(screen, image, threshold)
            if result:
                return result
            
        return result
    

class GameObject:
    def __init__(
            self,
            point: Point | None=None,
            template: Template | None=None
    ) -> None:
        self.point: Point | None = Point(**point) if point is not None else None
        self.template: Template | None = Template(**template) if template is not None else None
        self._cache: dict[str, ndarray] = {}

    @step
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
        if coords := self.template.compare_loop(screen, compare_methods.match_template):
            actions.input_tap(coords)
            screen_manager.reset_temp_screen()
            return True
        return False

    @screen_manager.with_screen
    def compare_part(self, screen, steps=0):
        cropped_screen = self.template.crop_screen(screen, steps=steps)
        return self.template.compare_loop(cropped_screen, compare_methods.ssim)
