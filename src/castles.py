from src.actions import Castle
from src.worksheet import get_column, get_sheet
from src.utils import object_from_str

def iter_castles():
    keys: list[str] = [cell.value for cell in get_sheet()[1] if cell.value is not None]  # type: ignore
    inp = input("enter from which castle do we start: ")  # first row is header

    def check_avatar() -> int:
        for i, name in enumerate(get_column("name"), start=2):
            assert isinstance(name, str), f"castle name {name} is not a string"
            if object_from_str(name).exists():
                return i
        else:
            raise RuntimeError("cannot find any castle on the screen")

    start_row = (
        check_avatar() if inp == ""
        else check_avatar() + 1 if inp == "next"
        else max(int(inp), 1) + 1 if inp.isdigit()
        else get_column("name").index(inp) + 2
    )
    for row in get_sheet().iter_rows(min_row=start_row):
        kwargs = dict(zip(keys, row))
        yield Castle(**kwargs)
