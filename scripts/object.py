from screen_objects import (
    Direction,
    SwipeSpeed,
    ScreenObject,
    tap_center,
    back,
    reset_screen,
)

from src.device import launch_instance
from src.utils import parse_instance
from src.objects import objects

launch_instance(parse_instance())

selected_object: ScreenObject | None = None

while command := input("Enter command: "):
    match command:
        case "exists":
            assert selected_object is not None, "exists should be called on some object"
            print(selected_object.exists())

        case "tap":
            assert selected_object is not None, "tap should be called on some object"
            print(selected_object.tap())

        case "tap_each":
            assert (
                selected_object is not None
            ), "tap_each should be called on some object"
            selected_object.tap_each()

        case "tap_center":
            tap_center()

        case "swipe":
            assert selected_object is not None, "swipe should be called on some object"
            direction = Direction.Up
            speed = SwipeSpeed.Turbo
            duration = float(input("Enter duration: "))
            result = selected_object.swipe(direction, speed, duration)
            print(result)

        case "cal":
            assert (
                selected_object is not None
            ), "calibrate should be called on some object"
            fixed = bool(input("fixed? "))
            region = inp if (inp := input("region: ")) else None
            n = int(inp) if (inp := input("n: ")) else None

            selected_object.calibrate(fixed, region, n)

        case cmd if cmd.startswith("spam"):
            assert selected_object is not None, "spam should be called on some object"
            [n, i] = cmd.split()[1:]
            result = selected_object.spam_tap(int(n), int(i))
            print(result)

        case cmd if cmd.startswith("tap"):
            assert selected_object is not None, "tap should be called on some object"
            n = cmd.split()[1]
            result = selected_object.tap_nth(int(n))
            print(result)

        case "count":
            assert selected_object is not None, "count should be called on some object"
            print(selected_object.count())

        case "back":
            back()

        case o:
            selected_object = objects[o]

    reset_screen()
