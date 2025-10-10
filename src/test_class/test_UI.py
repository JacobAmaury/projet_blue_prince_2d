import pygame
import sys
import time
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from UI import User_interface

def main():
    consumable = {'step': 50, 'coin': 3, 'gem': 2, 'key': 1, 'dice': 0}
    permanant_object = {'shovel': False, 'lockpick_kit': False, 'lucky_rabbit_foot': False, 'metal_detector': False, 'hammer': False}

    ui = User_interface((1280, 720), consumable, permanant_object)
    ui.initial_screen()
    
    clock = pygame.time.Clock()
    running = True
    t = 0

    ui.initial_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t += clock.get_time()
        if t > 1000:
            ui.consumable["step"] -= 1
            ui.update_item()
            t = 0

        if ui.consumable["step"] <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
