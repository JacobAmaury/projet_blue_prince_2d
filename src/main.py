import pygame
from ui import UI
from options import Options


pygame.init() #ini pygame
clock = pygame.time.Clock()
ui = UI()    #create and blit load_screen, load ressources for loadScreen
ui.load()   #display loadScreen while loading ressources
running = True
while running:
    running = ui.event_handler(pygame.event.get())
    clock.tick(Options.fps)
    pygame.display.update()