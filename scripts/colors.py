import os
import time
from cv2 import quality, imwrite, matchTemplate, TM_CCOEFF_NORMED, minMaxLoc

from my_packages.image_tools.template_manager import Templates
from my_packages.image_tools.screen_manager import _capture_gray
from my_packages.image_tools.image_analyzer import _cut

template = Templates.MINE.value.get_images()["farmstead_macro.png"]
screen = _capture_gray()
cut = _cut(screen, template, coords=(614, 1324))


imwrite("cut.png", cut)
imwrite("template.png", template)

tim1 = time.perf_counter()
result = quality.QualitySSIM_compute(template, cut)[0][0]
tim2 = time.perf_counter()
print(result)

