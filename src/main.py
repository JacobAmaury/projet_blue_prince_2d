import pygame
from ui import UI
from options import Options


pygame.init() #ini pygame
clock = pygame.time.Clock()
ui = UI()       #create window, load ressources for loadScreen
ui.load()       #display loadScreen while loading ressources
while True:
    ui.event_handler()
    clock.tick(Options.fps)
    pygame.display.update()