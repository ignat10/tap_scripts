from pathlib import Path


class GameObject:
    def compare(self, steps: int | None=None) -> bool: ...

    def tap(self, delay: float | None=None, steps: int | None=None, repeat: int | None=None) -> None: ...


def get_objects(data_path: Path) -> dict[str, GameObject]: ...
