from pathlib import Path
from os import listdir

screens = Path(r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\image_tools\screens")

screen_state_path = Path(r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\local\screen.png")
path: dict = {}

for name in listdir(screens):
    path[name] = screens / name
