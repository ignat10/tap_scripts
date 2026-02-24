from typing import Callable, Literal, TypeVar, ParamSpec, TYPE_CHECKING, Concatenate
from dataclasses import dataclass
from functools import wraps


if TYPE_CHECKING:
    from .game_object import GameObject
    import numpy as np


P = ParamSpec("P")
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


def step(func:
         Callable[Concatenate['GameObject', Coords, P], R] 
        ) -> Callable[Concatenate['GameObject', int, P], R]:
    @wraps(func)
    def wrapper(
            self: 'GameObject',
            *args: P.args,
            steps: int=0,
            **kwargs: P.kwargs
        ) -> R:
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
