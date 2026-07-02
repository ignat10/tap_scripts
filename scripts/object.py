from screen_objects import reset_screen, back

from src.objects import config
from src.utils import object_from_input, object_from_str

config()

obj = object_from_input()

while command := input("Enter command: "):
    match command:
        case "exists":
            print(obj.exists())

        case "tap":
            print(obj.tap())

        case "cal":
            fixed = bool(input("fixed? "))
            region = inp if (inp := input("region: ")) else None
            n = int(inp) if (inp := input("n: ")) else None

            obj.calibrate(fixed, region, n)

        case cmd if cmd.startswith("spam"):
            [n, i] = cmd.split()[1:]
            r = obj.spam_tap(int(n), int(i))
            print(r)

        case cmd if cmd.startswith("tap"):
            n = cmd.split()[1]
            r = obj.tap_nth(int(n))
            print(r)

        case "count":
            print(obj.count())

        case 'back':
            back()
            
        case o:
            obj = object_from_str(o)

    reset_screen()
