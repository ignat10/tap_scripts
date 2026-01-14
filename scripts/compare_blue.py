from my_packages.game_tools.objects import objects
from cv2 import imread, imshow, waitKey
book = objects["book"]
result = book.compare_part()
print(result)


screen = imread("screen.png")
imshow("ttsstt", screen)
crop = book._crop_screen(screen=screen, coords=book.coords)

imshow("tst", crop)
waitKey(0)