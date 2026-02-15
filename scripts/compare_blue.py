from src.game_object.objects import objects
from src.image_tools.compare_methods import numpy_diff

import numpy as np
from PIL import Image

book = objects["book"]


result = book.quiq_compare()
print(result)