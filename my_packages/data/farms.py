from pandas import read_excel

from .paths import FARMS_SHEET_PATH

farms_sheet = read_excel(FARMS_SHEET_PATH)
