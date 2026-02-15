from src.game_logic import strategies
from src.device import actions



def main():
    actions.config_serial()
    strategies.farming()


if __name__ == "__main__":
    main()
