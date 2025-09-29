# from float_coordinates import float_points, float_steps
#
# POCO_X7_PRO_RESOLUTION: tuple = [1220,  2712]
#
# for point in float_points:
#         print[[int[round[point[0] * POCO_X7_PRO_RESOLUTION[0]]], int[round[point[1] * POCO_X7_PRO_RESOLUTION[1]]]]]
# print[""]
# for step in float_steps:
#     index = int[input[f"{step}: "]]
#     print[int[round[step * POCO_X7_PRO_RESOLUTION[index]]]]
from frozendict import frozendict


points = frozendict({
    "take": [587, 1910],
    "close": [226, 2175],
    "lord":  [1130, 2068],
    "recall_all": [1000, 1000],
    "harvest": [226, 1763],
    "use": [599, 2633],
    "map": [113, 2599],
    "search": [1130, 2239],
    "mine_type": [678, 2345],
    "stone": [480, 2345],
    "wood": [289, 2345],
    "food": [113, 2345],
    "plus": [762, 2610],
    "minus": [130, 2610],
    "go_mine": [1017, 2627],
    "search_back": [890, 2150],
    "mine": [616, 1339],
    "gather": [875, 1309],
    "go": [1017, 2616],
    "back": [892, 2397],
    "favorites": [79, 2060],
    "favourites_back": [79, 170],
    "alliance_elite": [791, 300],
    "elite_blue":[429, 757],
    "elite_mine1": [429, 757],
    "gather_elite": [881, 1051],
    "vip": [1006, 1594],
    "avatar": [100, 100],
    "account": [203, 1243],
    "switch": [621, 1808],
    "login": [633, 1492],
    "google": [164, 840],
    "castle": [452, 1067],
    "confirm": [354, 1550],
})


STEPS = {
    "mine": -183,
    "mine_type": 0,
    "minimum_mine_type": -470,
    "elite_blue": 259,
    "google": 200,
    "castle": 135,
}

COLORS = {
    "search_back": [197, 170, 129, 255],
    "vip": [0, 132, 162, 255],
    "gather": [45, 43, 37, 255], # V
    "elite_blue": [56, 107, 134, 255],
    "gather_elite": [144, 72, 51, 255],
    "occupied": [55, 80, 18, 255],

}