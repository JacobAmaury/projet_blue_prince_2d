from map import Map
from inventory import Inventory

class Nav :
    def __init__(self,ui):
        self.ui = ui
    
    def new_game(self):
        self.inventory = Inventory(self.ui)
        self.map = Map(self.ui)
        self.ui.mainScreen()   #creates and blits main_screen

    class input :
        ## handlers for player inputs
        # keyboard inputs
        escape = lambda: print('escape')
        enter = lambda: print('enter')
        back = lambda: print('back')
        up = lambda: print('up')
        down = lambda: print('down')
        left = lambda: print('left')
        right = lambda: print('right')
