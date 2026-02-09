from src.game_tools.objects import objects
from src.image_tools.compare_methods import numpy_diff

import numpy as np
from PIL import Image

book = objects["book"]

temp = next(book.template.images)
scr = np.array(Image.open('screen.png'))
crp = book.template.crop_screen()

result = numpy_diff()
print(result)