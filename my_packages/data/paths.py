import os.path


class Path:
    def __init__(self):
        self._BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # packages
        self._SCREENS_DIR = os.path.join(self._BASE_DIR, 'image_tools', 'screens')
        self._DATA_DIR = os.path.join(self._BASE_DIR, 'data')
        self.screen_state_path = os.path.join(self._BASE_DIR, 'local', 'screen.png')
        self.farms_sheet_path = os.path.join(self._DATA_DIR, 'WAO_farms_data.xlsx')
        self.folder_names: frozenset[str] = frozenset(os.listdir(self._SCREENS_DIR))
        self.folder_paths: dict[str, str] = {folder_name: os.path.join(self._SCREENS_DIR, folder_name) for folder_name in self.folder_names}
        self.image_names: dict[str, frozenset[str]] = {folder_name: frozenset(os.listdir(folder_path)) for folder_name, folder_path in self.folder_paths.items()}
        self.image_paths: dict[str, frozenset[str]] = {folder_name: frozenset(os.path.join(folder_path, image_name) for image_name in self.image_names[folder_name]) for folder_name, folder_path in self.folder_paths.items()}


path = Path()
