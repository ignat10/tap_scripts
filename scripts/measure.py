from time import perf_counter
from src import objects


objects.config()

obj = objects.objects['city']


r = obj.find_object()

s = perf_counter()
t = obj.find_object()
e = perf_counter()
print(r)

print(f"took {e-s} seconds")