import pygame

from UI import UI
from Dev import Dev


screen = UI()
screen.initial_screen()

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #bg_image
    screen.update_item()
    screen.place_room_map(Dev.rooms) #This should be in this order to avoid flickering.

    clock.tick(60)
    pygame.display.update()

