from my_packages.adb_helpers.game_actions import Farm


def make_castles() -> list[Farm]:
    from my_packages.data.farms import farms_sheet
    from my_packages.utils.inputter import farm_number
    castles: list = []
    for row in farms_sheet.values[farm_number()::]:
        castles.append(Farm(*row))
    return castles
