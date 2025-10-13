import pygame
import os

from options import Options
from window import Window

class UI :
    #UI class must define all the Rect boxes for input management (mouse boxes)

    blit_current_window : lambda : None

    def __init__(self):
        #ini pygame
        pygame.init() #returns (nb loaded modules, nb failed)
        #window module initialisation
        self.window = Window()

    def load_screen(self):
        #create load window
        self.window.create_window()
        self.window.blit_load_screen()
        #set as current window for blitting
        self.blit_current_window = self.window.blit_load_screen

        #load game ressources
        self.window.load_images()

    def main_screen(self):
        self.window.blit_bg_items_rooms()
        #set as current window for blitting
        self.blit_current_window = self.window.blit_bg_items_rooms
        

    def event_handler(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                return  False
            if event.type == pygame.WINDOWRESIZED or event.type == pygame.WINDOWSIZECHANGED:
                self.window.W,self.window.H = event.x,event.y
                self.blit_current_window()
        return True
    
