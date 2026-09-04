from argparse import ArgumentParser

from screen_objects import screenshot


def log_raise(msg: str) -> None:
    screenshot()
    raise RuntimeError(f"{msg} Check screen.png for more details.")


def parse_instance():
    parser = ArgumentParser()
    parser.add_argument("instance", help="LDPlayer instance name")
    instance = parser.parse_args().instance
    assert instance is not None, f"required instance name"
    assert isinstance(instance, str)
    return instance
