from screen_objects import device_config

from src.castles import iter_castles


device_config()


castle = iter_castles().__next__()

action = castle.__getattribute__(input("enter castle action: "))

action()