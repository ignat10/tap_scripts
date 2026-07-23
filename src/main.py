from screen_objects import back, Direction, SwipeSpeed, reset_screen, tap_center

from src.actions import iter_castles
from src.device import config
from src.utils import object_from_input, object_from_str


def main():
    config()
    castles = iter_castles()
    match input("which script to run? {farming, grow, action, object}: "):
        case "grow":
            castle = castles.__next__()
            castle.close_ad()
            castle.check_level()
            castle.check_marches()
            for i in range(100):
                if i % 5 == 1:
                    castle.kill_monster()
                    castle.to_castle()
                if i % 15 == 2:
                    castle.events()
                if i % 20 == 3:
                    castle.claim_quest()
                castle.claim()
                castle.heal()
                castle.kingroad_task()
                print("made some kingroad task")

        case "farming":
            for castle in castles:
                castle.log_into_account()
                castle.close_ad()
                castle.claim()
                castle.heal()
                castle.lord_skills()
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
                    castle.to_castle()
                    castle.recruit()

        case "action":
            castle = next(iter_castles())

            while command := input("Enter action: "):
                func = getattr(castle, command)
                func()

        case "object":
            obj = object_from_input()

            while command := input("Enter command: "):
                match command:
                    case "exists":
                        print(obj.exists())

                    case "tap":
                        print(obj.tap())

                    case "tap_each":
                        obj.tap_each()

                    case "tap_center":
                        tap_center()

                    case "swipe":
                        direction = Direction.Up
                        speed = SwipeSpeed.Turbo
                        duration = float(input("Enter duration: "))
                        r = obj.swipe(direction, speed, duration)
                        print(r)

                    case "cal":
                        fixed = bool(input("fixed? "))
                        region = inp if (inp := input("region: ")) else None
                        n = int(inp) if (inp := input("n: ")) else None

                        obj.calibrate(fixed, region, n)

                    case cmd if cmd.startswith("spam"):
                        [n, i] = cmd.split()[1:]
                        r = obj.spam_tap(int(n), int(i))
                        print(r)

                    case cmd if cmd.startswith("tap"):
                        n = cmd.split()[1]
                        r = obj.tap_nth(int(n))
                        print(r)

                    case "count":
                        print(obj.count())

                    case 'back':
                        back()

                    case o:
                        obj = object_from_str(o)

                reset_screen()

        case com:
            raise IOError(f"unknown command: {com}")


if __name__ == "__main__":
    main()
