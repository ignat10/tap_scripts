from time import perf_counter
from src.utils import object_from_input


objects.config()

obj = object_from_input()


obj.exists()

s = perf_counter()
t = obj.exists()
e = perf_counter()

print(t)

print(f"took {e-s} seconds")
