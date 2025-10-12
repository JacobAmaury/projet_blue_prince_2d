import pygame

from ui import UI
from dev import Dev


ui = UI()
clock = pygame.time.Clock()
ui.load_screen()
running = True
while running:
    running = ui.event_handler(pygame.event.get())
    ui.main_screen()
    #bg_image
    # ui.update_item()
    # ui.place_room_map(Dev.rooms) #This should be in this order to avoid flickering.

    clock.tick(60)
    pygame.display.update()

