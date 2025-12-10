from os import path


_BASE_DIR = path.dirname(path.dirname(__file__))  # packages
_DATA_DIR = path.join(_BASE_DIR, 'data')

TEMPLATES_DIR = path.join(_DATA_DIR, 'templates')
FARMS_SHEET_PATH = path.join(_DATA_DIR, 'WAO_farms_data.xlsx')
