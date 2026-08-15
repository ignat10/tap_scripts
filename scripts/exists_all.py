from screen_objects import device_config

from src.objects import objects


device_config()

existing_objects = {
    name
    for name, obj in objects.items()
    if obj.exists()
}

print(existing_objects)
