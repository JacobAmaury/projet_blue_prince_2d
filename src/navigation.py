from map import Map
from inventory import Inventory

class Nav :
    def __init__(self,ui):
        self.ui = ui
    
    def new_game(self):
        self.inventory = Inventory(self.ui)
        self.map = Map(self.ui)
        self.ui.mainScreen()   #creates and blits main_screen