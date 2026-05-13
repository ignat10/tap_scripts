import pytest

from pathlib import Path

from src.paths import SAMPLES_DIR


@pytest.fixture
def files() -> set[Path]:
    return {path for path in SAMPLES_DIR.rglob("*") if path.is_file()}

@pytest.fixture
def png_files(files: set[Path]):
        return {path for path in files if path.suffix == '.png'}



def test_only_png(files: set[Path], png_files: set[Path]):
    assert files == png_files
