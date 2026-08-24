from argparse import ArgumentParser
from json import load

from screen_objects import start_app

from src.castles import iter_castles, release_all
from src.actions import Castle
from src.device import launch_instance
from src.paths import INSTANCES_PATH


def parse_args():
    parser = ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--instance", help="LDPlayer instance name")
    mode.add_argument(
        "--reset-busy",
        action="store_true",
        help="release all castles before starting workers",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.reset_busy:
        release_all()
        print("Released all castles")
        return

    instance_name = args.instance
    assert instance_name is not None
    with open(INSTANCES_PATH) as file:
        serials: dict[str, str] = load(file)
        serial = serials[instance_name]
    launch_instance(instance_name, serial)
    start_app()
    Castle.load()

    for castle in iter_castles():
        castle.grow()


if __name__ == "__main__":
    main()
