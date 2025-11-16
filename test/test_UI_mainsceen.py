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
        nav.inventory.add_permanent("Lockpick_Kit")
        nav.inventory.add_permanent("Shovel")
        nav.inventory.add_permanent("Lucky_Rabbits_Foot")
        nav.inventory.add_permanent("Power_Hammer")
        nav.inventory.add_permanent("Metal_Detector")
        nav.inventory.add_permanent('Coupon_Book')
        nav.inventory.add_permanent('fall_it_a_day')
        nav.map.add_room(Room("Passageway",2),(0, 0))
        room = Room("MusicRoom",r) ; room.message = "my room's message"
        nav.map.add_room(room,(x, y))   #add room (will fill the map)
        nav.player.move(x,y,r)
        nav.ui.screen.print('testing ... testing ... testing ...')
        x+=1; y+=1; r+=1
        r = r % 4 ; y = y % 9 ; x = x % 5   #protection overflow 
        t = 0
    

#Note doors are not rotated though the room is => weird, but works in main