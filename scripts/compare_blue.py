import timeit

from src.game_object.objects import objects


book = objects["blue"]


print(timeit.timeit('book.quick_compare()', setup = 'from src.game_object.objects import objects; book = objects["blue"]; book.quick_compare()', number=10000))
