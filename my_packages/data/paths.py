import os


screens = r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\image_tools\screens"
screen_state_path = r"D:\Documents\GitHub\PythonProject\tap_scripts\my_packages\local\screen.png"
path: dict[str, list[str]] = {}

for fol in os.listdir(screens):
    folder_path = os.path.join(screens, fol)
    path[fol] = []
    for img in os.listdir(folder_path):
        screen_path = os.path.join(folder_path, img)
        path[fol].append(screen_path)

print(path)