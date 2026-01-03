from cv2 import imread, imwrite, cvtColor, COLOR_BGR2GRAY
from numpy import ndarray
from cv2.quality import QualitySSIM_compute as ssim

from my_packages.image_tools import templates

corter = (152, 2000)
radius = 150
template = templates.BOOK


screen = cvtColor(imread("screen.png"), COLOR_BGR2GRAY)
image = template.get_images().__next__()

X = corter[0]
Y = corter[1]


def crop_screen(screen: ndarray, image: ndarray, corner: tuple[int, int]) -> ndarray:
    y, x = image.shape
    opposite_corner = (corner[0] + x, corner[1] + y)
    crop_screen = screen[corner[1]:opposite_corner[1], corner[0]:opposite_corner[0]]
    return crop_screen

matrix = []
for y in range(Y - radius, Y + radius):
    row = []
    for x in range(X - radius, X + radius):
        crop = crop_screen(screen, image, (x, y))
        similarity = round(ssim(crop, image)[0][0], 2)
        row.append(((x, y), similarity))
    matrix.append(row)


max = (0,0), 0.0
for y in matrix:
    for x in y:
        if x[1] > max[1]:
            max = x

print("Max similarity:", max)
