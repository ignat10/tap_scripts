from time import sleep


from ..adb_tools.adb_actions import input_tap


class Point(tuple):
    def __new__(cls, coords: tuple, offstep: int=0):
        obj = super().__new__(cls, coords)
        obj.offstep = offstep
        return obj

    def __call__(self, index: int, times: int=0):
        lst = list(self)
        lst[index] += self.offstep * times
        return Point(tuple(lst))

    def click(self) -> None:
        input_tap(self)

    def wait_and_click(self, delay=0.5):
        sleep(delay)
        self.click()

    def repeat_click(self, times: int):
        for _ in range(times):
            self.click()
                
            
class Points:
    take = Point((587, 1910))
    close = Point((226, 2175))
    lord = Point((1130, 2068))
    recall_all = Point((1000, 1000))
    harvest = Point((226, 1763))
    use = Point((599, 2633))
    map = Point((113, 2599))
    search = Point((1130, 2239))
    mine_type = Point((678, 2345), offstep= -200)
    stone = Point((480, 2345))
    wood = Point((289, 2345))
    food = Point((113, 2345))
    plus = Point((762, 2610))
    minus = Point((130, 2610))
    go_mine = Point((1017, 2627))
    search_back = Point((890, 2150))
    mine = Point((616, 1339), offstep= -183)
    gather = Point((875, 1309))
    go = Point((1017, 2616))
    back = Point((892, 2397))
    favorites = Point((79, 2060))
    favorites_back = Point((79, 170))
    alliance_elite = Point((791, 300))
    elite_blue = Point((421, 757), offstep=259)
    elite_mine1 = Point((429, 757))
    gather_elite = Point((881, 1051))
    vip = Point((1006, 1594))
    avatar = Point((100, 100))
    account = Point((203, 1243))
    switch = Point((621, 1808))
    login = Point((633, 1492))
    google = Point((164, 840), offstep=200)
    castle = Point((452, 1067), offstep=135)
    confirm = Point((354, 1550))
