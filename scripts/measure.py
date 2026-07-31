from time import perf_counter

from src.device import config
from src.utils import object_from_input


config()

obj = object_from_input()

ss = perf_counter()
obj.exists()
ee = perf_counter()

s = perf_counter()
t = obj.exists()
e = perf_counter()

diff = e - s
screencap = ee - ss - diff

print(f"took {diff} seconds. screencap: {screencap} seconds")
