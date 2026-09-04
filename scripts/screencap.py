from screen_objects import screenshot

from src.device import launch_instance
from src.utils import parse_instance

launch_instance(parse_instance())

screenshot()
