import os
import time
from cv2 import quality, imwrite, matchTemplate, TM_CCOEFF_NORMED, minMaxLoc

from my_packages.image_tools.image_manager import Templates
from my_packages.image_tools.screen_manager import _capture_gray
from my_packages.image_tools.image_analyzer import _cut

template = Templates.MINE.value.get()["new_one.png"]
screen = _capture_gray()
cut = _cut(screen, template, coords=(614, 1324))

minmax = matchTemplate(screen, template, TM_CCOEFF_NORMED)
a, b, c, d = minMaxLoc(minmax)
print(a, b, c, d)

imwrite("cut.png", cut)
imwrite("template.png", template)

tim1 = time.perf_counter()
result = quality.QualitySSIM_compute(template, cut)[0][0]
tim2 = time.perf_counter()
print(result)
