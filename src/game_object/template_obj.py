from pathlib import Path
from typing import Iterator, Callable, TypeVar

from PIL import Image
import numpy as np

from ..paths import TEMPLATES_DIR
from . import point_obj

R = TypeVar("R")

class Template:
    def __init__(
            self,
            path: str,
            threshold: float
        ) -> None:
        self.path: Path = Path(path)
        self.threshold: float = threshold
        self._cache: dict[str, np.ndarray] = {}

    @property
    def images(self) -> Iterator[np.ndarray]:
        for file_path in (TEMPLATES_DIR / self.path).iterdir():
            file_name = file_path.name
            if file_name not in self._cache:
                self._cache[file_name] = np.array(Image.open(file_path), dtype=np.uint8)
            yield self._cache[file_name]

    @point_obj.step
    def crop_screen(self, screen: np.ndarray, coords: point_obj.Coords) -> np.ndarray:
        y, x = next(self.images).shape
        opposite_corner = point_obj.Coords(coords.x + x, coords.y + y)
        crop_screen = screen[coords.y:opposite_corner.y, coords.x:opposite_corner.x]
        return crop_screen

    
    def compare_loop(self, screen: np.ndarray, compare_method: Callable[[np.ndarray, np.ndarray, float], R]) -> R:
        threshold = self.threshold
        result: R | None = None
        for image in self.images:
            result = compare_method(screen, image, threshold)
            if result:
                return result
             
        return result