from my_packages.game_tools import strategies, loaders
from my_packages.device import actions



def main():
    actions.config_serial()
    loaders.load_game_objects()
    strategies.farming()


if __name__ == "__main__":
    main()
