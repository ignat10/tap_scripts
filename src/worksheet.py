from openpyxl import load_workbook

from src.paths import FARMS_SHEET_PATH

workbook = load_workbook(FARMS_SHEET_PATH)
sheet = workbook.active
if sheet is None:
    raise ValueError("No active sheet in workbook")


def save_workbook() -> None:
    workbook.save(FARMS_SHEET_PATH)
