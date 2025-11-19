# from float_coordinates import float_points, float_steps
#
# POCO_X7_PRO_RESOLUTION: tuple = (1220,  2712)
#
# for point in float_points:
#         print((int(round(point(0) * POCO_X7_PRO_RESOLUTION(0))), int(round(point(1) * POCO_X7_PRO_RESOLUTION(1)))))
# print("")
# for step in float_steps:
#     index = int(input(f"{step}: "))
#     print(int(round(step * POCO_X7_PRO_RESOLUTION(index))))


class Point(tuple):
    def __new__(cls, coords: tuple, gap: int=0):
        obj = super().__new__(cls, coords)
        obj.gap = gap
        return obj

    def __call__(self, index: int | None = None, times: int = 0):
        match index:
            case None:
                return tuple(self)
            case 0:
                return (self[0] + self.gap * times, self[1])
            case 1:
                return (self[0], self[1] + self.gap * times)
            case _:
                exit("Index must be 0 or 1!")
        


DEVICE_IP = "192.168.0.192"
class Points:
    take = Point((587, 1910))
    close = Point((226, 2175))
    lord = Point((1130, 2068))
    recall_all = Point((1000, 1000))
    harvest = Point((226, 1763))
    use = Point((599, 2633))
    map = Point((113, 2599))
    search = Point((1130, 2239))
    mine_type = Point((678, 2345), gap= -200)
    stone = Point((480, 2345))
    wood = Point((289, 2345))
    food = Point((113, 2345))
    plus = Point((762, 2610))
    minus = Point((130, 2610))
    go_mine = Point((1017, 2627))
    search_back = Point((890, 2150))
    mine = Point((616, 1339), gap= -183)
    gather = Point((875, 1309))
    go = Point((1017, 2616))
    back = Point((892, 2397))
    favorites = Point((79, 2060))
    favorites_back = Point((79, 170))
    alliance_elite = Point((791, 300))
    elite_blue = Point((421, 757), gap=259)
    elite_mine1 = Point((429, 757))
    gather_elite = Point((881, 1051))
    vip = Point((1006, 1594))
    avatar = Point((100, 100))
    account = Point((203, 1243))
    switch = Point((621, 1808))
    login = Point((633, 1492))
    google = Point((164, 840), gap=200)
    castle = Point((452, 1067), gap=135)
    confirm = Point((354, 1550))
