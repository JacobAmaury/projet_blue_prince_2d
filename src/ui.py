import pygame

from options import Options
from display import Display
from navigation import Nav

class UI :
    #UI class must define all the Rect boxes for input management (mouse boxes)

    refresh_current_display : lambda : None     #build and blit

    def __init__(self):
        #ini pygame
        pygame.init() #returns (nb loaded modules, nb failed)
        #display initialisation
        self.display = Display()

    def load(self):
        # todo : add ui.event_handler calls for pseudo-async effect (responsive window resizing)
        #create and load display
        self.display.create_window()
        self.display.build_and_blit_loadScreen()
        pygame.display.flip()   #blit before loadind ressources
        #set as current display for blitting
        self.refresh_current_display = self.display.build_and_blit_loadScreen

        #load game ressources
        self.display.load_images()

        #initialise Navigation (=game controller)
        self.nav = Nav(self)

        #start a new game
        self.nav.new_game()

    def build_mainScreen(self):
        self.display.build_bg_screen()
        self.display.build_items(self.nav.inventory.consumables)
        self.display.build_rooms(self.nav.map)

    def blit_mainScreen(self):
        self.display.blit_bg_screen()
        self.display.blit_items(self.nav.inventory.permanant_objects) 
        self.display.blit_rooms(self.nav.map)

    def build_and_blit_mainScreen(self):
        self.build_mainScreen()
        self.blit_mainScreen()

    def mainScreen(self):
        self.build_and_blit_mainScreen()
        #set as current screen for blitting
        self.refresh_current_display = self.build_and_blit_mainScreen

    def update_consumables(self):
        self.display.build_items(self.nav.inventory.consumables)
        self.blit_mainScreen()

    def update_permanents(self):
        self.display.blit_items(self.nav.inventory.permanant_objects)
        self.blit_mainScreen() # useless if we cannot lose a permanent object

    def update_map(self):
        self.display.build_rooms(self.nav.map)
        self.display.blit_rooms(self.nav.map)

    def event_handler(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                return  False
            if event.type == pygame.WINDOWRESIZED or event.type == pygame.WINDOWSIZECHANGED:
                self.display.W,self.display.H = event.x,event.y
                Options.display_ratio_enforced = False
                self.refresh_current_display()
        return True
    
