import pygame
from ui import UI
from options import Options
from navigation import Nav


pygame.init()                       #ini pygame
clock = pygame.time.Clock()
nav = Nav.ini(UI)
while True:
    UI.event_listener()
    clock.tick(UI.fps)
    pygame.display.update()
