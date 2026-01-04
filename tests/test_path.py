import pytest

from pathlib import Path

from my_packages.data.paths import TEMPLATES_DIR
from my_packages.image_tools import templates



def get_listdir_paths(full_path: Path = Path(TEMPLATES_DIR)):
    listdir_items = full_path.iterdir()

    result = set()
    for item in listdir_items:
        if item.is_dir():
            result.update(get_listdir_paths(item))
        else:
            result.add(full_path.relative_to(TEMPLATES_DIR))
    return result


@pytest.fixture
def get_listdir_paths_fixture():
    return get_listdir_paths()


@pytest.fixture
def get_templates_path_fixture():
    return {
        template.path
        for attribute in dir(templates)
        if isinstance((template := getattr(templates, attribute)), templates.Template)
        }


def test_templates_enum_matches_dirs(
        get_listdir_paths_fixture,
        get_templates_path_fixture
        ):
    listdir_paths: set[Path] = get_listdir_paths_fixture
    templates_path: set[Path] = get_templates_path_fixture
    assert listdir_paths == templates_path
