from cv2 import imread, imwrite, cvtColor, COLOR_BGR2GRAY, quality
from numpy import array, ndarray


from my_packages.image_tools.template_manager import Templates


ssim = quality.QualitySSIM_compute


screen = cvtColor(imread("screen.png"), COLOR_BGR2GRAY)
template = Templates.BOOK.value
image = template.get_images().values().__iter__().__next__()

corter = (570, 1280)
X = corter[0]
Y = corter[1]
radius = 50

matrix = array([
    [
        round(ssim(image, template.crop_screen(screen))[0][0], 2)
        for x in range(X, X + radius)
    ]
    for y in range(Y, Y + radius)
])

print(matrix)
