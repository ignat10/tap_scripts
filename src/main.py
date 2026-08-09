from screen_objects import start_app

from src.actions import iter_castles, Castle
from src.device import config


def main():
    config()
    castles = iter_castles()
    start_app()
    Castle.load()
    Castle.close_ad()
    match input("which script to run: farming or grow?: "):
        case "grow":
            for castle in castles:
                castle.log_into_account()
                castle.close_ad()
                castle.check_level()
                castle.check_marches()
                castle.claim_mail()
                for i in range(100):
                    if i % 49 == 0:
                        castle.claim_rss()
                    if i % 40 == 0:
                        castle.upgrade_lord_skills()
                    if i % 5 == 1:
                        castle.kill_monster()
                        castle.close_ad()
                    # if i % 15 == 2:
                    #     castle.events()
                    if i % 20 == 3:
                        castle.claim_quest()
                    castle.claim()
                    castle.heal()
                    if castle.has_speed and not castle.need_rss:
                        castle.kingroad_task()
                    elif not castle.build():
                        castle.recruit()
                        castle.to_map()
                        if castle.free_marches() != 0 and castle.is_enough_troops and not castle.get_elite_mine():
                            castle.get_std_mine()
                        while castle.free_marches() >= 1 and castle.is_enough_troops:
                            castle.get_std_mine()
                        print("don't know what to do in this castle.")
                        break
                    print("made some kingroad task")

        case "farming":
            for castle in castles:
                castle.log_into_account()
                castle.close_ad()
                castle.claim()
                castle.claim_rss()
                castle.heal()
                castle.use_lord_skills()
                castle.to_map()

                for i in range(castle.free_marches() - 1):  # - 1 for elite mine
                    if castle.is_enough_troops:
                        castle.get_std_mine()
                    else:
                        break
                else:
                    if castle.get_elite_mine() is False:
                        castle.get_std_mine()

                    if castle.free_marches() == 0:
                        castle.is_enough_troops = True

                if not castle.is_enough_troops:
                    castle.close_ad()
                    castle.recruit()

        case com:
            raise IOError(f"unknown command: {com}")


if __name__ == "__main__":
    main()
