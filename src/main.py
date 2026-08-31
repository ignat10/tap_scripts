from argparse import ArgumentParser

from screen_objects import start_app

from src.castles import iter_castles
from src.actions import Castle
from src.device import launch_instance


def parse_instance():
    parser = ArgumentParser()
    parser.add_argument("instance", help="LDPlayer instance name")
    instance = parser.parse_args().instance
    assert instance is not None, f"required instance name"
    assert isinstance(instance, str)
    return instance


def main():
    instance = parse_instance()
    launch_instance(instance)
    start_app()
    Castle.load()

    for castle in iter_castles():
        castle.grow()


if __name__ == "__main__":
    main()
