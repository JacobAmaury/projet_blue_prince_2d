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
        ui.nav.inventory.change_perm("Shovel",not("Shovel" in ui.nav.inventory.permanents))
        ui.nav.inventory.change_perm("Lockpick_Kit",not("Lockpick_Kit" in ui.nav.inventory.permanents))
        ui.nav.inventory.change_perm("Lucky_Rabbits_Foot",not("Lucky_Rabbits_Foot" in ui.nav.inventory.permanents))
        ui.nav.inventory.change_perm("Metal_Detector",not("Metal_Detector" in ui.nav.inventory.permanents))
        ui.nav.inventory.change_perm("Power_Hammer",not("Power_Hammer" in ui.nav.inventory.permanents))
        ui.nav.map.add_room("Security",(8, -1,-1))
        ui.nav.map.add_room("Mechanarium",(0, 0,2))
        ui.nav.map.add_room("MusicRoom",(1+x, y,r))   #add room (will fill the map)
        ui.nav.map.move_door(1+x,y,r)
        x+=1; y+=1; r+=1
        t = 0
    

