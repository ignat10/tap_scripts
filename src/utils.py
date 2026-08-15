from screen_objects import screenshot


def log_raise(msg: str) -> None:
    screenshot()
    raise RuntimeError(f"{msg} Check screen.png for more details.")
