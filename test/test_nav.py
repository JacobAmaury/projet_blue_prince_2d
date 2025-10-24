import __src_path   #set path ../src

#main
import pygame
from basic_ui import UI                   # pyright: ignore[reportMissingImports]
from options import Options         # pyright: ignore[reportMissingImports]


pygame.init()                       #ini pygame
clock = pygame.time.Clock()
ui = UI()
while True:
    ui.event_listener()
    clock.tick(Options.fps)
    pygame.display.update()