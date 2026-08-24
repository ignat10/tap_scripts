from pathlib import Path

_ROOT_DIR = Path(__file__).parent.parent
_DATA_DIR = _ROOT_DIR / 'data'

SAMPLES_DIR = _DATA_DIR / 'samples'
REGIONS_DIR = _DATA_DIR / 'regions'
INSTANCES_PATH = _DATA_DIR / 'instances.json'
CASTLES_DB_PATH = _DATA_DIR / 'castles.db'
