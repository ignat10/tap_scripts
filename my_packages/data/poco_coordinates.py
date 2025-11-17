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


class PointData(tuple):
    def __new__(cls, coords: tuple, gap: float | None=None):
        obj = super().__new__(cls, coords)
        obj.gap = gap
        return obj
    

DEVICE_IP = "192.168.0.192"
class Point:
    take = PointData((587, 1910))
    close = PointData((226, 2175))
    lord = PointData((1130, 2068))
    recall_all = PointData((1000, 1000))
    harvest = PointData((226, 1763))
    use = PointData((599, 2633))
    map = PointData((113, 2599))
    search = PointData((1130, 2239))
    mine_type = PointData((678, 2345), gap=-200)
    stone = PointData((480, 2345))
    wood = PointData((289, 2345))
    food = PointData((113, 2345))
    plus = PointData((762, 2610))
    minus = PointData((130, 2610))
    go_mine = PointData((1017, 2627))
    search_back = PointData((890, 2150))
    mine = PointData((616, 1339), gap=-183)
    gather = PointData((875, 1309))
    go = PointData((1017, 2616))
    back = PointData((892, 2397))
    favorites = PointData((79, 2060))
    favorites_back = PointData((79, 170))
    alliance_elite = PointData((791, 300))
    elite_blue = PointData((421, 757), gap=259)
    elite_mine1 = PointData((429, 757))
    gather_elite = PointData((881, 1051))
    vip = PointData((1006, 1594))
    avatar = PointData((100, 100))
    account = PointData((203, 1243))
    switch = PointData((621, 1808))
    login = PointData((633, 1492))
    google = PointData((164, 840), gap=200)
    castle = PointData((452, 1067), gap=135)
    confirm = PointData((354, 1550))
