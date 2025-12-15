from os import system

from my_packages.adb_tools.device_actions import serial

system(f"adb -s {serial} exec-out screencap -p > screen.png")
