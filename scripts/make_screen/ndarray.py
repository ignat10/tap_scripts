import cv2
from numpy import frombuffer, uint8

from my_packages.adb_tools.device_actions import screencap

raw_bytes = screencap()
screen_bytes = frombuffer(raw_bytes, uint8)
screen = cv2.imdecode(screen_bytes, cv2.IMREAD_COLOR)
cv2.imwrite("screen_from_ndarray.png", screen)
