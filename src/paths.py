from pathlib import Path



_ROOT_DIR = Path(__file__).parent.parent
_DATA_DIR = _ROOT_DIR / 'data'


TEMPLATES_DIR = _DATA_DIR / 'templates'
FARMS_SHEET_PATH = _DATA_DIR / 'WAO_farms_data.xlsx'
GAME_OBJECTS = _DATA_DIR / 'game_objects.json'
