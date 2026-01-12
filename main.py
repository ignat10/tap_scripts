from my_packages.game_tools import strategies, objects
from my_packages.device import actions



def main():
    actions.config_serial()
    objects.load_game_objects()
    strategies.farming()


if __name__ == "__main__":
    main()
