import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'src')) #import from ../src

#test
import pygame
from ui import UI               # pyright: ignore[reportMissingImports] 
from options import Options     # pyright: ignore[reportMissingImports] 

t = 0
pygame.init() #ini pygame
clock = pygame.time.Clock()
ui = UI()
ui.load()
while True:
    ui.event_handler()
    
    #test
    t += clock.get_time()
    if t > 1000:
        ui.nav.map.add_room("Security",(2, -1))
        ui.nav.inventory.change_consumable("steps",-1)
        ui.nav.inventory.change_perm("Shovel",not(ui.nav.inventory.perm_objects["Shovel"]))
        ui.nav.inventory.change_perm("Lockpick_Kit",not(ui.nav.inventory.perm_objects["Lockpick_Kit"]))
        ui.nav.inventory.change_perm("Lucky_Rabbits_Foot",not(ui.nav.inventory.perm_objects["Lucky_Rabbits_Foot"]))
        ui.nav.inventory.change_perm("Metal_Detector",not(ui.nav.inventory.perm_objects["Metal_Detector"]))
        ui.nav.inventory.change_perm("Power_Hammer",not(ui.nav.inventory.perm_objects["Power_Hammer"]))
        t = 0
    

    clock.tick(Options.fps)
    pygame.display.update()
