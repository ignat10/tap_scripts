import pytest

from typing import get_args
from pathlib import Path

from src.paths import TEMPLATES_DIR
from src.game_tools import objects



@pytest.fixture
def literal_names() -> set[str]:
    return set(get_args(objects.GameObjectNames))


@pytest.fixture
def data_names() -> set[str]:
    return set(objects.objects)


def get_listdir_paths(full_path: Path = Path(TEMPLATES_DIR)) -> set[Path]:
    listdir_items = full_path.iterdir()

    result = set()
    for item in listdir_items:
        if item.is_dir():
            result.update(get_listdir_paths(item))
        else:
            result.add(full_path.relative_to(TEMPLATES_DIR))
    return result


@pytest.fixture
def listdir_paths() -> set[Path]:
    return get_listdir_paths()


@pytest.fixture
def templates_paths() -> set[Path]:
    return {
        path
        for object in objects.objects.values()
        if (path := object.path) is not None
        }


def test_data_names_contains_literal(
        data_names,
        literal_names
        ):
    assert literal_names == data_names


def test_templates_enum_matches_dirs(
        listdir_paths,
        templates_paths
        ):
    assert listdir_paths == templates_paths
