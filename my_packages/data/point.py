from time import sleep
from enum import Enum


from ..device import actions



class Axis(Enum):
    X = 0
    Y = 1


class Point(tuple):
    axis: Axis | None
    offset: int | None

    def __new__(cls, coords: tuple[int, int], offset: tuple[int, Axis] | None = None):
        obj = super().__new__(cls, coords)
        if offset is not None:
            obj.offset = offset[0]
            obj.axis = offset[1]
        return obj

    def __call__(self, times: int=0):
        lst = list(self)
        lst[self.axis.value] += self.offset * times
        return Point(tuple(lst))

    def click(self) -> None:
        actions.input_tap(self)

    def wait_and_click(self, delay=0.5):
        sleep(delay)
        self.click()

    def repeat_click(self, times: int):
        for _ in range(times):
            self.click()
