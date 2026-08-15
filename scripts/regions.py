from screen_objects import device_config, get_regions

from src.paths import REGIONS_DIR


device_config()

regions = get_regions(REGIONS_DIR)

while key := input("enter region name: "):
    regions[key].calibrate()
