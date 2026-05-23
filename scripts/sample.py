from screen_objects import reset_screen

from src.objects import config, objects
from src.utils import object_from_input

config()

obj = object_from_input()

while command := input("Enter command: "):
    match command:
        case "exists":
            print(obj.exists())

        case 'add':
            obj.add_sample()
            
        case 'reset':
            reset_screen()
            
        case _:
            print("Invalid command")
