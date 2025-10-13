import pygame

from ui import UI
from dev import Dev
from options import Options
from rooms import Rooms


ui = UI()
clock = pygame.time.Clock()
ui.load_screen()
ui.main_screen_create()
running = True
while running:
    running = ui.event_handler(pygame.event.get())
    ui.main_screen_blit()
    Rooms.update_rooms(ui)
    # ui.update_item()
    # ui.place_room_map(Dev.rooms) #This should be in this order to avoid flickering.

    clock.tick(Options.fps)
    pygame.display.update()

