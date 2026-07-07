from src.device import config
from src.actions import iter_castles

config()

castle = next(iter_castles())

while command := input("Enter action: "):
    func = getattr(castle, command)
    func()