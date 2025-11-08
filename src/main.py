import pygame
from ui import UI
from navigation import Nav


pygame.init()                       #ini pygame
nav = Nav.ini(UI)
while True:
    UI.event_listener()
    UI.clock.tick(UI.fps)
    pygame.display.update()
