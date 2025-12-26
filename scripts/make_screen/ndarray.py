from cv2 import imdecode, IMREAD_COLOR, imwrite
from numpy import frombuffer, uint8

from my_packages.adb_tools.device_actions import screencap

raw_bytes = screencap()
screen_bytes = frombuffer(raw_bytes, uint8)
screen = imdecode(screen_bytes, IMREAD_COLOR)
imwrite("screen_from_ndarray.png", screen)