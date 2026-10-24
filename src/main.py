from screen_objects import start_app

from src.castles import iter_castles, release
from src.utils import parse_instance
from src.device import launch_instance


def main():
    instance = parse_instance()
    launch_instance(instance)
    start_app()
    castles = iter_castles()
    castle = next(castles, None)
    if castle is None:
        return
    try:
        castle.load()
        castle.log_into_account()
    except:
        release(castle.name)
        raise

    while True:
        assert castle is not None
        name_old = None
        name_new = None
        try:
            name_old = castle.name
            castle.grow()
            castle = next(castles, None)
            if castle is None:
                break
            name_new = castle.name
            castle.log_into_account()
        except Exception as e:
            raise

        finally:
            assert name_old is not None
            release(name_old)
            if name_new is not None:
                release(name_new)




if __name__ == "__main__":
    main()
