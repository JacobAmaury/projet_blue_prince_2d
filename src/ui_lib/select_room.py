"""Room selection menu for the player to choose a room to enter.

This module provides the SelectRoom class which displays a menu of three
available rooms with their properties (gem cost, rotation) and allows the
player to select one, or reroll the selection using a dice (if available).
"""

import pygame

from .image import ImageSimple, ImageReapeated
from .event_handler import EventHandler
from .window import Screen


class SelectRoom(Screen):
    """Display a room selection menu with three rooms and reroll option.
    
    Overlays the main screen with a darkened background and displays three
    available rooms to choose from. Each room shows its name, gem cost,
    and rotation. The fourth selection option (index 3) is a reroll button
    that uses dice from inventory.
    
    Layout constants (all as ratios of window width/height):
        X_ROOMS (float): Horizontal starting position of rooms.
        Y_ROOMS (float): Vertical starting position of rooms.
        X_STEP (float): Horizontal spacing between room displays.
        X_OFF_GEM (float): Horizontal offset for gem cost relative to room.
        Y_OFF_GEM (float): Vertical offset for gem cost relative to room.
        SIZE_GEM (float): Size of gem icon.
        SIZE_ROOM (float): Room image scale.
    
    Attributes:
        rooms (list): List of three Room objects to display.
        room_choice (int): Currently selected choice index (0-3).
        room_images (list): Cached ImageSimple instances for each room.
        dice_count (int): Number of dice in player inventory.
    """
    room_images = [None]*3
    X_ROOMS = 0.309     #ratio of W
    Y_ROOMS = 0.173     #ratio of H
    X_STEP = 0.187
    X_OFF_GEM = 0.7   #ratio of case W
    Y_OFF_GEM = 0.01   #ratio of case W
    SIZE_GEM = 0.035 #ratio of W
    SIZE_ROOM = 0.173

    def __init__(self, rooms):
        """Initialize the room selection menu with the given rooms.
        
        Args:
            rooms (list): List of three Room objects to display for selection.
        
        Returns:
            None
        """
        Screen.__init__(self)
        self.mainscreen = self.window.ui.screen
        self.rooms = rooms
        self.room_choice = 0
        #import images from loadscreen
        self.bg_image = ImageSimple(Screen.selectionmenu_bg_img)
        self.dice_image = ImageSimple(Screen.consumable_imgs['dice'])
        self.gem_image = ImageReapeated(Screen.consumable_imgs['gem'])
        self.update()

    def select(self):
        """Display the room selection menu and handle user navigation and selection.

        Handles left/right navigation between 3 rooms and a reroll option (4 choices),
        enter to select, and spacebar as an alternative select. Escape or up/down
        cancel the menu. If the player selects the reroll option (index 3) but has
        no dice, a message is displayed and the menu remains open.

        Returns:
            int: Room index (0-2) for selected room, -1 if cancelled (escape),
                 or 3 if reroll selected (requires at least 1 dice).
        """
        # Why not just return index ?
        class MenuHandler(EventHandler):
            @staticmethod
            def escape() : 
                self.running=False
                self.room_choice = -1
                self.blit()
            @staticmethod
            def left():
                self.room_choice = (self.room_choice - 1) % 4 
                self.blit()
            @staticmethod
            def right():
                self.room_choice = (self.room_choice + 1)  %4
                self.blit()
            @staticmethod
            def enter() : 
                if self.room_choice != 3 :
                    self.running = False  #return selection
                else : 
                    if self.dice_count >= 1 :
                        self.running = False  #close menu to rerun selection_menu
                        return 3           # return 3
                    else :
                        self.print("Can't reroll, no dice left !")
            ##optionnal handlers : not in the game specifications (easier debugg), can be removed later
            @staticmethod
            def space():
                MenuHandler.enter()
            @staticmethod
            #cancel if go back or up
            def down():
                MenuHandler.escape()
            def up():
                MenuHandler.escape()
        self.event_handler = MenuHandler
        event_listener = self.window.ui.event_listener
        self.running = True
        while self.running:
            event_listener()
            pygame.display.flip()
        return self.room_choice

    def build(self):
        """Build and scale all visual elements for the room selection menu.
        
        Prepares room images, gem cost overlays, dark filter, and dice display.
        
        Returns:
            None
        """
        self.mainscreen.build()
        self.size = self.window.size
        W, H = self.size
        Y_ROOMS = self.Y_ROOMS ; X_ROOMS = self.X_ROOMS ; X_STEP = self.X_STEP
        SIZE_ROOM = self.SIZE_ROOM
        X_OFF_GEM = self.X_OFF_GEM; Y_OFF_GEM = self.Y_OFF_GEM; SIZE_GEM = self.SIZE_GEM
        font = pygame.font.Font(None, int(H * 0.05))
        #gem cost sticker
        gem_image = self.gem_image
        gem_image.scale((int(W * SIZE_GEM), int(W * SIZE_GEM)))
        self.gem_texts = []
        #image building
        self.bg_image.smoothscale((W, H))
        for id,room in enumerate(self.rooms):
            room_img = Screen.room_imgs[room.name]
            room_img = pygame.transform.rotate(room_img, room.rotation*90)
            room_image = ImageSimple(room_img)
            room_image.smoothscale((int(W * SIZE_ROOM), int(H * SIZE_ROOM * 16/9)))
            room_image.position = (W * (X_ROOMS + X_STEP*id), H * Y_ROOMS)
            self.room_images[id]=(room_image)
            #gem sticker
            if(room.data['gem'] < 0):
                gem_image.positions.append((W * (X_ROOMS + X_STEP*(id + X_OFF_GEM)), H *(Y_ROOMS + Y_OFF_GEM)))
                self.gem_texts.append(font.render(str(- room.data['gem']), True, (255, 255, 255)))
        
        #black filter
        dark_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 180))
        self.dark_overlay = dark_overlay
        #dice
        dice_image = self.dice_image
        dice_image.scale((int(W * 0.04), int(W * 0.04)))
        dice_image.position = (W * 0.87, H * 0.2)
        self.dice_image = dice_image
        #dice count
        dice_x, dice_y = dice_image.position
        self.dice_count_position = (dice_x + W * 0.05, dice_y + H * 0.005)
        self.dice_count = self.mainscreen.player.inventory.consumables["dice"]
        self.dice_text = font.render(str(self.dice_count), True, (255, 255, 255))

    
    def blit(self):
        """Render the room selection menu overlay to the buffer.
        
        Draws main screen, dark overlay, room images with gem costs, dice display,
        and a white selection border around the currently selected item.
        
        Returns:
            None
        """
        W, H = self.size
        Y_ROOMS = self.Y_ROOMS ; X_ROOMS = self.X_ROOMS ; X_STEP = self.X_STEP
        buffer = self.buffer
        self.mainscreen.blit() #draw mainscreen
        buffer.blit(self.dark_overlay, (0, 0))
        buffer.blit(self.bg_image.scaled, (0, 0))
        for room_image in self.room_images:
            room_image.blit(buffer)
        for id,gem_text in enumerate(self.gem_texts):
            position = self.gem_image.positions[id]
            buffer.blit(self.gem_image.scaled, position)  
            buffer.blit(gem_text, (position[0] - W*0.008, position[1] + H*0.0125))  
            
        #dice display
        self.dice_image.blit(buffer)
        buffer.blit(self.dice_text, self.dice_count_position)
        #white rectangle : recalculate position (and size for dice) if move
        if self.room_choice != 3:
            id = self.room_choice
            self.rect = pygame.Rect(W * (X_ROOMS + X_STEP*id), H * Y_ROOMS, int(W * 0.174), int(H * 0.174 * 16/9))
        else:
            self.rect = pygame.Rect(W * 0.87, H * 0.2, int(W * 0.04), int(H * 0.04 * 16/9))
        pygame.draw.rect(buffer, (255, 255, 255), self.rect, width=4)
    
