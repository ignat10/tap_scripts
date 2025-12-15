from cv2.quality import QualitySSIM_compute
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, imshow, waitKey

from my_packages.image_tools.image_manager import Templates
from my_packages.image_tools.image_analyzer import _cut


screen = cvtColor(imread("screen.png"), COLOR_BGR2GRAY)
template = Templates.MINE.value.get()["night_farm.png"]

center = (570, 1280)
radius = 20

matrix: list[list[tuple[tuple[int, int], float]]] = []

for y in range(center[1] - radius, center[1] + radius):
    row = []
    for x in range(center[0] - radius, center[0] + radius):
        cut = _cut(screen, template, coords=(x, y))
        result = QualitySSIM_compute(template, cut)[0][0]
        print(f"Position: ({x}, {y}) - SSIM: {result}")
        row.append(((x, y), round(result, 2)))
    matrix.append(row)

print(matrix)

max_result: tuple[tuple[int, int], float] = ((0, 0), -1.0)
for row in matrix:
    for item in row:
        if item[1] > max_result[1]:
            max_result = item
        
print(max_result)


from cv2 import imwrite

imwrite("cut_at_max.png", _cut(screen, template, coords=max_result[0]))
