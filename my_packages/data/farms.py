from pandas import read_excel

from my_packages.image_tools.image_manager import farms_sheet_path

farms_sheet = read_excel(farms_sheet_path)
