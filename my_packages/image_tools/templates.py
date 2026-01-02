from pathlib import Path


from .template_manager import Template



ADS = Template(Path("ads"), 0.9)
BLUE = Template(Path("blue"), 0.8)
BOOK = Template(Path("book"), 0.8, coords=(88, 2069))
CITIES = Template(Path("cities"), 0.8)
FAVOURITES = Template(Path("favourites"), 0.8)
GATHER = Template(Path("gather"), 0.8)
LOAD = Template(Path("load"), 0.9)
MAIN_MENUS = Template(Path("main_menus"), 0.9)
SEARCH_BAR = Template(Path("search_menus"), 0.9)
XS = Template(Path("xs"), 0.8)
LEO = Template(Path("avatars/leo"), 0.8)
LORD = Template(Path("avatars/lord"), 0.8)
MINE = Template(Path("mines"), 0.8, coords=(614, 1324))
