from src.castles import iter_castles
from src.device import launch_instance
from src.main import parse_instance


launch_instance(parse_instance())


castle = iter_castles().__next__()

action = castle.__getattribute__(input("enter castle action: "))

action()
