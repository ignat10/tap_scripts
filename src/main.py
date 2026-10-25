from screen_objects import start_app

from src.castles import iter_castles, release, get_castle_name_by_avatar, get_castle
from src.utils import parse_instance, log_raise
from src.device import launch_instance
from src.status import check_avatar


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
        avatar = check_avatar()
        if avatar is None:
            log_raise("Loaded, but no avatar was found.")
        name = get_castle_name_by_avatar(avatar)
        assert name is not None
        print(f"Currently logged into {name}")
        account = get_castle(name)['account']
        castle.log_into_account(account)
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
            old_account = castle.account
            assert old_account is not None
            castle = next(castles, None)
            if castle is None:
                break
            name_new = castle.name
            castle.log_into_account(old_account)
        except Exception:
            raise

        finally:
            assert name_old is not None
            release(name_old)
            if name_new is not None:
                release(name_new)




if __name__ == "__main__":
    main()
