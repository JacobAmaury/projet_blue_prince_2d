import UI
import pygame

screen1 = UI.User_interface((1920,1080), 0, 0)
screen1.initial_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #bg_image
    screen1.update_item()
    pygame.display.update()

