import __src_path   #set path ../src
""" This test executes the game in the terminal. It is meant to separate ui developpement from navigation.
    Feel free to change basic_ui based on Nav's needs.
"""

#main
import pygame
from basic_ui import UI             # pyright: ignore[reportMissingImports]
from options import Options         # pyright: ignore[reportMissingImports]
from navigation import Nav      # pyright: ignore[reportMissingImports]


pygame.init()                       #ini pygame
clock = pygame.time.Clock()
nav = Nav(UI)
while True:
    UI.event_listener()
    clock.tick(Options.fps)
    pygame.display.update()