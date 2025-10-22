import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'src')) #import from ../src

#test
import pygame
from ui import UI               # pyright: ignore[reportMissingImports] 
from options import Options     # pyright: ignore[reportMissingImports] 

t = 0

clock = pygame.time.Clock()
ui = UI()    #create and blit load_screen, load ressources for loadScreen
ui.load()   #display loadScreen while loading ressources
running = True
while running:
    running = ui.event_handler(pygame.event.get())
    
    #test
    t += clock.get_time()
    if t > 1000:
        ui.nav.map.add_room("Security",(2, -1))
        ui.nav.inventory.change_consumable("step",-1)
        ui.nav.inventory.change_permanents("shovel",not(ui.nav.inventory.permanant_objects["shovel"]))
        ui.nav.inventory.change_permanents("lockpick_kit",not(ui.nav.inventory.permanant_objects["lockpick_kit"]))
        ui.nav.inventory.change_permanents("lucky_rabbit_foot",not(ui.nav.inventory.permanant_objects["lucky_rabbit_foot"]))
        ui.nav.inventory.change_permanents("metal_detector",not(ui.nav.inventory.permanant_objects["metal_detector"]))
        ui.nav.inventory.change_permanents("hammer",not(ui.nav.inventory.permanant_objects["hammer"]))
        t = 0
    

    clock.tick(Options.fps)
    pygame.display.update()
