from time import sleep



class Point(tuple):
    def __new__(cls, coords: tuple, offset: int=0):
        obj = super().__new__(cls, coords)
        obj.offset = offset
        return obj

    def __call__(self, index: int, times: int=0):
        lst = list(self)
        lst[index] += self.offset * times
        return Point(tuple(lst))

    def click(self) -> None:
        from ..device import actions
        actions.input_tap(self)

    def wait_and_click(self, delay=0.5):
        sleep(delay)
        self.click()

    def repeat_click(self, times: int):
        for _ in range(times):
            self.click()
