import __src_path   #set path ../src


from map import Map                 # pyright: ignore[reportMissingImports]
from inventory import Inventory     # pyright: ignore[reportMissingImports]

class Nav :
    def __init__(self,UI):
        Nav.ui = UI(Nav)
        Nav.inventory = Inventory(Nav.ui)
        Nav.map = Map(Nav.ui)
        Nav.ui.mainScreen()   #creates and blits main_screen


