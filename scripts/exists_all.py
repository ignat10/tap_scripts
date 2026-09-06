from pprint import pprint

from src.device import launch_instance
from src.utils import parse_instance
from src.objects import objects

launch_instance(parse_instance())

existing_objects = {name for name, obj in objects.items() if obj.exists()}

pprint(existing_objects)
