import pygame
from ui import UI
from options import Options
from navigation import Nav


pygame.init()                       #ini pygame
clock = pygame.time.Clock()
nav = Nav(UI)
while True:
    UI.event_listener()
    clock.tick(Options.fps)
    pygame.display.update()
