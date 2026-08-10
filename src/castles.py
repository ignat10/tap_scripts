from openpyxl.worksheet.worksheet import Worksheet

from src.actions import Castle
from src.worksheet import sheet
from src.utils import object_from_str

def iter_castles():
    assert isinstance(sheet, Worksheet)

    keys: list[str] = [cell.value for cell in sheet[1] if cell.value is not None]  # type: ignore
    inp = input("enter from which castle do we start: ")  # first row is header

    def check_avatar():
        assert isinstance(sheet, Worksheet)

        for cell in sheet['A'][1:]:
            if not isinstance(cell.value, str):
                raise ValueError(f"castle name {cell.value} is not a string")
            if object_from_str(cell.value).exists():
                return cell.row
        else:
            raise RuntimeError("cannot find any castle on the screen")

    match inp:
        case "":
            start_row = check_avatar()
        case "next":
            start_row = check_avatar() + 1
        case n if n.isdigit():
            start_row = max(int(n), 1) + 1  # because of header
        case name:
            start_row = next(
                i for i, cell in enumerate(sheet['A'][1:], start=2)
                if cell.value == name
            )
    for row in sheet.iter_rows(min_row=start_row):
        kwargs = dict(zip(keys, row))
        yield Castle(**kwargs)
