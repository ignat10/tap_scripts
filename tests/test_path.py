import pytest

from pathlib import Path

from my_packages.data.paths import TEMPLATES_DIR
from my_packages.image_tools.template_manager import Templates



def get_paths(full_path: Path = Path(TEMPLATES_DIR)):
    listdir_items = full_path.iterdir()

    result = set()
    for item in listdir_items:
        if item.is_dir():
            result.update(get_paths(item))
        else:
            result.add(full_path.relative_to(TEMPLATES_DIR))
    return result


@pytest.fixture
def get_paths_fixture():
    return get_paths()


def test_templates_enum_matches_dirs(get_paths_fixture):
    listdir_paths: set[Path] = get_paths_fixture
    Templates_enum: set[Path] = {item.value.path for item in Templates}

    assert listdir_paths == Templates_enum, (
        f"expected {Templates_enum - listdir_paths}, \nfound {listdir_paths - Templates_enum}"
    )