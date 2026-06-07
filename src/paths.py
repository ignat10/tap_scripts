from pathlib import Path



_ROOT_DIR = Path(__file__).parent.parent


DATA_DIR = _ROOT_DIR / 'data'
SAMPLES_DIR = DATA_DIR / 'samples'
FARMS_SHEET_PATH = DATA_DIR / 'WAO_farms_data.xlsx'
OBJECTS_PATH = DATA_DIR / 'game_objects.json'
