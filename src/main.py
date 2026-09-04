from screen_objects import start_app

from src.castles import iter_castles
from src.actions import Castle
from src.utils import parse_instance
from src.device import launch_instance


def main():
    instance = parse_instance()
    launch_instance(instance)
    start_app()
    Castle.load()

    for castle in iter_castles():
        castle.grow()


if __name__ == "__main__":
    main()
