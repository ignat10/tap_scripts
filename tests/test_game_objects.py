import pytest

from typing import get_args

from src import objects



@pytest.fixture
def literal_names() -> set[str]:
    return set(get_args(objects.GameObjectNames))


@pytest.fixture
def data_names() -> set[str]:
    return set(objects.objects)


def test_data_names_contains_literal(
        data_names,
        literal_names
        ):
    assert literal_names == data_names
