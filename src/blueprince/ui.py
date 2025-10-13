import pygame
import os

from options import Options
from window import Window
from inventory import Inventory
from rooms import Rooms

class UI :
    #UI class must define all the Rect boxes for input management (mouse boxes)

    build_current_window : lambda : None
    blit_current_window : lambda : None

    def __init__(self):
        #ini pygame
        pygame.init() #returns (nb loaded modules, nb failed)
        #window module initialisation
        self.window = Window()

    def load_screen(self):
        #create load window
        self.window.create_window()
        self.window.build_load_screen()
        self.window.blit_load_screen()
        pygame.display.flip()   #fast blit : cause it is the first screen
        #set as current window for blitting
        self.build_current_window = self.window.build_load_screen
        self.blit_current_window = self.window.blit_load_screen

        #load game ressources
        self.window.load_images()

    def main_screen_create(self):
        self.window.build_main_screen()

    def main_screen_blit(self):
        self.window.blit_main_screen()
        #set as current window for blitting
        self.build_current_window = self.window.build_main_screen
        self.blit_current_window = self.window.blit_main_screen

    def change_consumables(self):
        self.window.build_items(Inventory.consumables)

    def change_map(self):
        self.window.build_rooms(Rooms.rooms)

    def event_handler(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                return  False
            if event.type == pygame.WINDOWRESIZED or event.type == pygame.WINDOWSIZECHANGED:
                self.window.W,self.window.H = event.x,event.y
                Options.window_ratio_enforced = False
                self.build_current_window()
                self.blit_current_window()
        return True
    
