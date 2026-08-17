from argparse import ArgumentParser
from json import load

from screen_objects import start_app

from src.castles import iter_castles, Castle
from src.device import launch_instance
from src.paths import INSTANCES_PATH


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--instance", help="LDPlayer instance name")
    return parser.parse_args()


def main():
    instance_name = parse_args().instance
    with open(INSTANCES_PATH) as file:
        serials: dict[str, str] = load(file)
        serial = serials[instance_name]
    launch_instance(instance_name, serial)
    start_app()
    Castle.load()

    command = input("which script to run: farming or grow?: ")

    for castle in iter_castles():
        castle.__getattribute__(command)()


if __name__ == "__main__":
    main()
