from src.actions import Castle
from src.castles import iter_castles


def test_iter_castles():
    castles = iter_castles()

    for castle in castles:
        assert isinstance(castle, Castle)
