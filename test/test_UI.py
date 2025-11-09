import __src_path   #set path ../src


#test variables
t = 0
x,y,r = 1,0,0


#main
import pygame
from ui import UI                   # pyright: ignore[reportMissingImports]
from navigation import Nav           # pyright: ignore[reportMissingImports]
from player import Room           # pyright: ignore[reportMissingImports]

pygame.init()                       #ini pygame
nav = Nav.ini(UI)
while True:
    UI.event_listener()
    UI.clock.tick(UI.fps)
    pygame.display.update()


    
#test
    t += UI.clock.get_time()
    if t > 1000:
        nav.inventory.change_consumable("steps",-1)
        nav.inventory.change_perm("Lockpick_Kit",not("Lockpick_Kit" in nav.inventory.permanents))
        nav.inventory.change_perm("Shovel",not("Shovel" in nav.inventory.permanents))
        nav.inventory.change_perm("Lucky_Rabbits_Foot",not("Lucky_Rabbits_Foot" in nav.inventory.permanents))
        nav.inventory.change_perm("Power_Hammer",not("Power_Hammer" in nav.inventory.permanents))
        nav.inventory.change_perm("Metal_Detector",not("Metal_Detector" in nav.inventory.permanents))
        nav.map.add_room(Room("Passageway",2),(0, 0))
        nav.map.add_room(Room("MusicRoom",r),(x, y))   #add room (will fill the map)
        nav.player.move(x,y,r)
        x+=1; y+=1; r+=1
        r = r % 4 ; y = y % 9 ; x = x % 5   #protection overflow 
        t = 0
    

