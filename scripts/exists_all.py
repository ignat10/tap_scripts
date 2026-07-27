from src.device import config
from src.objects import objects

config()

existing_objects = {
    name
    for name, obj in objects.items()
    if obj.exists()
}

print(existing_objects)
