from screen_objects import device_config, Direction, SwipeSpeed, ScreenObject, tap_center, back, reset_screen

from src.objects import objects


device_config()

obj: ScreenObject | None = None

while command := input("Enter command: "):
    match command:
        case "exists":
            assert obj is not None, "exists should be called on some object"
            print(obj.exists())

        case "tap":
            assert obj is not None, "tap should be called on some object"
            print(obj.tap())

        case "tap_each":
            assert obj is not None, "tap_each should be called on some object"
            obj.tap_each()

        case "tap_center":
            tap_center()

        case "swipe":
            assert obj is not None, "swipe should be called on some object"
            direction = Direction.Up
            speed = SwipeSpeed.Turbo
            duration = float(input("Enter duration: "))
            r = obj.swipe(direction, speed, duration)
            print(r)

        case "cal":
            assert obj is not None, "calibrate should be called on some object"
            fixed = bool(input("fixed? "))
            region = inp if (inp := input("region: ")) else None
            n = int(inp) if (inp := input("n: ")) else None

            obj.calibrate(fixed, region, n)

        case cmd if cmd.startswith("spam"):
            assert obj is not None, "spam should be called on some object"
            [n, i] = cmd.split()[1:]
            r = obj.spam_tap(int(n), int(i))
            print(r)

        case cmd if cmd.startswith("tap"):
            assert obj is not None, "tap should be called on some object"
            n = cmd.split()[1]
            r = obj.tap_nth(int(n))
            print(r)

        case "count":
            assert obj is not None, "count should be called on some object"
            print(obj.count())

        case 'back':
            back()

        case o:
            obj = objects[o]

    reset_screen()