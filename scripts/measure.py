from json import load
from time import perf_counter

from src.device import launch_instance
from src.utils import parse_instance
from src.objects import objects


launch_instance(parse_instance())

screencap_timer = perf_counter()
objects.values().__iter__().__next__().exists() # screencap
screencap = perf_counter() - screencap_timer

with open("data/objects.json") as f:
    data = load(f)
assert isinstance(data, dict)

fixed_timer = not_fixed_timer = 0.0

def exists_all():
    global fixed_timer, not_fixed_timer
    for name, obj in objects.items():
        start = perf_counter()
        obj.exists()
        end = perf_counter()
        delta = end - start
        if data[name][0] is None: # if coords are not fixed:
            not_fixed_timer += delta
        else:
            fixed_timer += delta

exists_all()
fixed_load, not_fixed_load = fixed_timer, not_fixed_timer
fixed_timer = not_fixed_timer = 0.0
exists_all()
load = fixed_load - fixed_timer + not_fixed_load - not_fixed_timer

print(f"fixed took {fixed_timer}. not fixed: {not_fixed_timer}, load: {load}, screencap: {screencap}")
