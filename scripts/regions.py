from screen_objects import get_regions

from src.device import launch_instance
from src.utils import parse_instance
from src.paths import REGIONS_DIR

launch_instance(parse_instance())

regions = get_regions(REGIONS_DIR)

while key := input("enter region name: "):
    regions[key].calibrate()
