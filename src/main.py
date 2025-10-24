import pygame
from ui import UI
from options import Options


pygame.init()                       #ini pygame
clock = pygame.time.Clock()
ui = UI()
while True:
    ui.event_listener()
    clock.tick(Options.fps)
    pygame.display.update()
