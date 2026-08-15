import pytest

from typing import get_args

from src.objects import ScreenObjectNames, objects



@pytest.fixture
def literal_names() -> set[str]:
    return set(get_args(ScreenObjectNames))


@pytest.fixture
def data_names() -> set[str]:
    return set(objects.keys())


def test_data_names_contains_literal(
        data_names: set[str],
        literal_names: set[str]
        ):
    assert literal_names == data_names
