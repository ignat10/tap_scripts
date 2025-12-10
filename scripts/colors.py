
import time
from cv2 import quality, imshow, waitKey, imwrite
from my_packages.image_tools.screen_manager import _capture_gray
from my_packages.image_tools.image_manager import get_images, Templates
from my_packages.image_tools.image_analyzer import _cut

book = get_images(Templates.BOOK)["book.png"]
scr = _capture_gray()
cut = _cut(scr, book, coords=(88, 2069))
print(cut.shape)
print(book.shape)
imshow("cut", cut)
imshow("book", book)

imwrite("cut.png", cut)
imwrite("book.png", book)

waitKey(15000)
tim1 = time.perf_counter()
result = quality.QualitySSIM(book, cut)
tim2 = time.perf_counter()
print(result)
print(tim2 - tim1)
