from src.actions import iter_castles

castle = next(iter_castles())

while command := input("Enter action: "):
    func = getattr(castle, command)
    func()