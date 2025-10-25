from map import Map
from inventory import Inventory

class Nav :
    def __init__(self,UI):
        Nav.ui = UI(Nav)
        Nav.new_game()     #start a new game

    @classmethod
    def new_game(cls):
        cls.inventory = Inventory(cls.ui)
        cls.map = Map(cls.ui)
        cls.ui.mainScreen()   #creates and blits main_screen


