import pygame

from options import Options
from display import Display


class UI :
    #UI class must define all the Rect boxes for input management (mouse boxes)

    build_current_screen : lambda : None
    blit_current_screen : lambda : None

    def __init__(self,Rooms,Inventory):
        #ini pygame
        pygame.init() #returns (nb loaded modules, nb failed)
        #display initialisation
        self.display = Display()
        UI.instance = self  #needed to avoid circular imports
        self.Rooms = Rooms  #needed to avoid circular imports
        self.Inventory = Inventory #needed to avoid circular imports

    def load_screen(self):
        #create load display
        self.display.create_window()
        self.display.build_load_screen()
        self.display.blit_load_screen()
        pygame.display.flip()   #fast blit : cause it is the first screen
        #set as current display for blitting
        self.build_current_screen = self.display.build_load_screen
        self.blit_current_screen = self.display.blit_load_screen

        #load game ressources
        self.display.load_images(self.Rooms)

    def build_main_screen(self):
        self.display.build_bg_screen()
        self.display.build_items(self.Inventory.consumables)
        self.display.build_rooms(self.Rooms)

    def blit_main_screen(self):
        self.display.blit_bg_screen()
        self.display.blit_items(self.Inventory.permanant_objects) 
        self.display.blit_rooms(self.Rooms)

    def main_screen_load(self):
        self.build_main_screen()
        self.blit_main_screen()
        #set as current screen for blitting
        self.build_current_screen = self.build_main_screen
        self.blit_current_screen = self.blit_main_screen

    def update_consumables(self):
        self.display.build_items(self.Inventory.consumables)
        self.blit_main_screen()

    def update_permanents(self):
        self.display.blit_items(self.Inventory.permanant_objects)
        self.blit_main_screen() # useless if we cannot lose a permanent object

    def update_map(self):
        self.display.build_rooms(self.Rooms)
        self.display.blit_rooms(self.Rooms)

    def event_handler(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                return  False
            if event.type == pygame.WINDOWRESIZED or event.type == pygame.WINDOWSIZECHANGED:
                self.display.W,self.display.H = event.x,event.y
                Options.display_ratio_enforced = False
                self.build_current_screen()
                self.blit_current_screen()
        return True
    
