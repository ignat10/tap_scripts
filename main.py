from my_packages.game_tools import strategies
from my_packages.device import actions

def main():
    actions.config_serial()
    strategies.farming()


if __name__ == "__main__":
    main()
