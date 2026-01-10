from os import system

from my_packages.device.actions import serial

system(f"adb -s {serial} exec-out screencap -p > screen.png")
