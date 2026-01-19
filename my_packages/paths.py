from pathlib import Path



_BASE_DIR = Path(__file__).parent.parent  # my_packages
_DATA_DIR = _BASE_DIR / 'data'


TEMPLATES_DIR = _DATA_DIR / 'templates'
FARMS_SHEET_PATH = _DATA_DIR / 'WAO_farms_data.xlsx'
GAME_OBJECTS = _DATA_DIR / 'game_objects.json'
