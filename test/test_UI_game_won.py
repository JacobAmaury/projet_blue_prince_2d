import __src_path   # set path ../src

import pygame
from ui import UI                   # pyright: ignore[reportMissingImports]
from navigation import Nav           # pyright: ignore[reportMissingImports]

# test variables
t = 0
menu_open = False

pygame.init()
clock = pygame.time.Clock()
nav = Nav.ini(UI)

start_time = pygame.time.get_ticks()

while True:
    UI.event_listener()
    clock.tick(UI.fps)
    pygame.display.update()

    t += clock.get_time()
    if t > 1000:
        choix = UI.game_won()
        t = 0


pygame.quit()
