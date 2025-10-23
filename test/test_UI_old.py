import pygame
import sys
import time
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ui import UI

def main():
    consumable = {'step': 50, 'coin': 3, 'gem': 2, 'key': 1, 'dice': 0}
    permanant_objects = {'shovel': True, 'lockpick_kit': False, 'lucky_rabbit_foot': True, 'metal_detector': False, 'hammer': True}

    rooms = {
        "Mechanarium": [(1, 0),(2,-2)],
        "MusicRoom": [(2, 0)],
        "Security": [(2, -1)]
    }

    ui = UI((1920, 1080), consumable, permanant_objects)
    
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
            ui.consumables["step"] -= 1
            ui.permanant_objects["shovel"] = not(ui.permanant_objects["shovel"])
            ui.permanant_objects["lockpick_kit"] = not(ui.permanant_objects["lockpick_kit"])
            ui.permanant_objects["lucky_rabbit_foot"] = not(ui.permanant_objects["lucky_rabbit_foot"])
            ui.permanant_objects["metal_detector"] = not(ui.permanant_objects["metal_detector"])
            ui.permanant_objects["hammer"] = not(ui.permanant_objects["hammer"])
            t = 0

        
        ui.update_item()
        ui.place_room_map(rooms) #This should be in this order to avoid flickering.

        if ui.consumables["step"] <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
