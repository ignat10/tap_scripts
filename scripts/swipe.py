from screen_objects import swipe_center, SwipeSpeed, Direction

from src.device import launch_instance
from src.utils import parse_instance

launch_instance(parse_instance())

match input("swipe speed: "):
    case "slow":
        speed = SwipeSpeed.Slow
    case "normal":
        speed = SwipeSpeed.Normal
    case "fast":
        speed = SwipeSpeed.Fast
    case "turbo":
        speed = SwipeSpeed.Turbo
    case _:
        raise Exception("Invalid input")

match input("swipe direction: "):
    case "down":
        direction = Direction.Down
    case "up":
        direction = Direction.Up
    case "left":
        direction = Direction.Left
    case "right":
        direction = Direction.Right
    case _:
        raise Exception("Invalid input")

duration = float(input("swipe duration: "))

swipe_center(direction, speed, duration)
