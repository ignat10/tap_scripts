from typing import Iterator


from openpyxl import load_workbook


from ..data.paths import FARMS_SHEET_PATH
from ..utils.inputter import inputter



sheet = load_workbook(FARMS_SHEET_PATH).active


def generator(type_) -> Iterator:
    for row in sheet.iter_rows(min_row=inputter("enter from which google do we start: ", 1) + 1, values_only=True):
        yield type_(*row)
