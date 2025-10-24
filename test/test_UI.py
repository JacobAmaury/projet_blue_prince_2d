import __src_path   #set path ../src


#test variables
t = 0
x,y,r = 0,0,0


#main
import pygame
from ui import UI                   # pyright: ignore[reportMissingImports]
from options import Options         # pyright: ignore[reportMissingImports]


pygame.init()                       #ini pygame
clock = pygame.time.Clock()
ui = UI()
while True:
    ui.event_listener()
    clock.tick(Options.fps)
    pygame.display.update()

    
#test
    t += clock.get_time()
    if t > 1000:
        ui.nav.inventory.change_consumable("steps",-1)
        ui.nav.inventory.change_perm("Shovel",not(ui.nav.inventory.perm_objects["Shovel"]))
        ui.nav.inventory.change_perm("Lockpick_Kit",not(ui.nav.inventory.perm_objects["Lockpick_Kit"]))
        ui.nav.inventory.change_perm("Lucky_Rabbits_Foot",not(ui.nav.inventory.perm_objects["Lucky_Rabbits_Foot"]))
        ui.nav.inventory.change_perm("Metal_Detector",not(ui.nav.inventory.perm_objects["Metal_Detector"]))
        ui.nav.inventory.change_perm("Power_Hammer",not(ui.nav.inventory.perm_objects["Power_Hammer"]))
        ui.nav.map.add_room("Security",(8, -1,-1))
        ui.nav.map.add_room("Mechanarium",(0, 0,2))
        ui.nav.map.add_room("MusicRoom",(1+x, y,r))   #add room (will fill the map)
        ui.update_door(1+x,y,r)
        x+=1; y+=1; r+=1
        t = 0
    

