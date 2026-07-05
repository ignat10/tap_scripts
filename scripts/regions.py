from screen_objects import get_regions

from src.objects import config
from src.paths import REGIONS_DIR

config()
regions = get_regions(REGIONS_DIR)

while key := input("enter region name: "):
    regions[key].calibrate()
