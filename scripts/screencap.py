from os import system

from src.device import actions
actions.config_serial()

system(f"adb -s {actions.serial} exec-out screencap -p > screen.png")
