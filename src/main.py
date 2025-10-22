import pygame
from ui import UI
from options import Options
from map import Map
from inventory import Inventory


ui = UI(Map,Inventory)
clock = pygame.time.Clock()
ui.load_screen()    #creates and blits load_screen
ui.main_screen_load()   #creates and blits main_screen
running = True
while running:
    running = ui.event_handler(pygame.event.get())

    clock.tick(Options.fps)
    pygame.display.update()