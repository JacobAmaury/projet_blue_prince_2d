import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame
from ui import UI
from options import Options
from map import Map
from inventory import Inventory

t = 0

ui = UI(Map,Inventory)
clock = pygame.time.Clock()
ui.load_screen()    #creates and blits load_screen
ui.main_screen_load()   #creates and blits main_screen
running = True
while running:
    running = ui.event_handler(pygame.event.get())
    
    #test
    t += clock.get_time()
    if t > 1000:
        Map.add_room("Security",(2, -1))
        Inventory.change_consumable("step",-1)
        Inventory.change_permanents("shovel",not(Inventory.permanant_objects["shovel"]))
        Inventory.change_permanents("lockpick_kit",not(Inventory.permanant_objects["lockpick_kit"]))
        Inventory.change_permanents("lucky_rabbit_foot",not(Inventory.permanant_objects["lucky_rabbit_foot"]))
        Inventory.change_permanents("metal_detector",not(Inventory.permanant_objects["metal_detector"]))
        Inventory.change_permanents("hammer",not(Inventory.permanant_objects["hammer"]))
        t = 0
    

    clock.tick(Options.fps)
    pygame.display.update()
