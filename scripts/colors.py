from time import perf_counter
from cv2 import quality, imwrite

from my_packages.image_tools.template_manager import Templates
from my_packages.image_tools.screen_manager import get_screen

template = Templates.MINE.value
screen = get_screen()
cut = template.crop_screen(screen)


imwrite("cut.png", cut)
imwrite("template.png", template)

tim1 = perf_counter()
result = quality.QualitySSIM_compute(template, cut)[0][0]
tim2 = perf_counter()
print(result)

