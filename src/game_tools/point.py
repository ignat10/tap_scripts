from typing import Literal, Callable, TypeVar, ParamSpec, Concatenate, overload, TYPE_CHECKING
from dataclasses import dataclass
from functools import wraps


if TYPE_CHECKING:
    from .game_object import GameObject

T = TypeVar("T")
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


# @overload
# def step(func: Callable[Concatenate[GameObject, Coords, P], R]) -> Callable[..., R]: ...
    
def step(
    func: Callable[Concatenate[GameObject, Coords, P], R]
    ) -> Callable[Concatenate[GameObject, int, P]]:
    @wraps(func)
    def wrapper(
            self: GameObject,
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
                
        return func(self, moved_coords, *args, **kwargs)
    return wrapper
