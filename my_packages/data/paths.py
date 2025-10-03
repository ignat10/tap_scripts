from os import listdir

from pathlib import Path

screens = Path(r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\image_tools\screens")

screen_state_path = Path(r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\local\screen.png")
path: dict[str, list[Path]] = {}

for fol in listdir(screens):
    path[fol] = []
    for img in listdir(screens / fol):
        path[fol].append(screens / fol / img)

print(path)