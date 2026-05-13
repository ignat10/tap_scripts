from screen_objects import reset_screen

from src.objects import device_config, objects

device_config()

name = input("Enter object name: ")

obj = objects[name] # type: ignore

while command := input("Enter command: "):
    match command:
        case "find":
            print(obj.find_object())

        case "comp":
            print(obj.compare())

        case 'add':
            obj.add_sample()
            
        case 'reset':
            reset_screen()
            
        case _:
            print("Invalid command")
