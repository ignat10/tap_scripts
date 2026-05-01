from screen_objects import reset_screen

from src.objects import objects

name = input("Enter object name: ")

object = objects[name] # type: ignore

while command := input("Enter command: "):
    match command:
        case "find":
            print(object.find_object())

        case "comp":
            print(object.compare())

        case 'add':
            object.add_sample()
            
        case 'reset':
            reset_screen()
            
        case _:
            print("Invalid command")
