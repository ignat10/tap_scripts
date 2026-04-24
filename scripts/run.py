from src.actions import iter_castles

iterator = iter_castles()



castle = iterator.__next__()




castle.log_into_account()
