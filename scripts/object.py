from screen_objects import reset_screen, back

from src.objects import config
from src.utils import object_from_input

config()

obj = object_from_input()

while command := input("Enter command: "):
    match command:
        case "exists":
            print(obj.exists())

        case "tap":
            print(obj.tap())

        case cmd if cmd.startswith("spam"):
            [n, i] = cmd.split()[1:]
            obj.spam_tap(int(n), int(i))
            
        case 'back':
            back()
            
        case _:
            print("Invalid command")

    reset_screen()
