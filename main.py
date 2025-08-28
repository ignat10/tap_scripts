# local
from my_packages.adb_tools.adb_config import connect_adb
from my_packages.adb_tools.game_actions import *

def main():
    connect_adb()
    farming()


if __name__ == "__main__":
    main()