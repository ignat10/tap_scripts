from time import sleep


from .actions import castle_generator



castles = castle_generator()


def farming() -> None:
    for castle in castles:
        castle.log_into_account()
        castle.go_outside()
        castle.lord_skills()

        castle.get_std_mine()
        castle.get_std_mine()
        if not castle.get_elite_mine():
            castle.get_std_mine()
        castle.get_std_mine()


def seconds():
    for castle in castles:
        castle.log_into_account()
        sleep(15)
