import pygame

from .image import ImageFull, ImageTransparant
from .event_handler import EventHandler
from .window import Screen

class SelectionMenu(Screen):
    room_images = [None]*3
    X_RATIO = 0.309     #ratio of W
    Y_RATIO = 0.173     #ratio of H
    X_STEP_RATIO = 0.187

    def __init__(self,rooms):
        Screen.__init__(self)
        self.mainscreen = self.window.ui.screen
        self.rooms = rooms
        self.room_choice = 0
        #import images from loadscreen
        self.bg_image = ImageTransparant(Screen.selectionmenu_bg_img)
        self.dice_image = ImageTransparant(Screen.consumable_imgs['dice'])
        self.build_selection_menu()

    def selection(self):
        """
        Returns the rank of the selected room, -1 if cancelled, 3 if reroll
        """ 
        # Why not just return index ?
        class MenuHandler(EventHandler):
            @staticmethod
            def escape() : 
                self.running=False
                self.room_choice = -1
            @staticmethod
            def left():
                self.room_choice = (self.room_choice - 1) % 4 
            @staticmethod
            def right():
                self.room_choice = (self.room_choice + 1)  %4
            @staticmethod
            def enter() : 
                if self.room_choice != 3 :
                    self.running = False  #close menu with selection
                else : 
                    if self.dice_count >= 1 :
                        self.running = False  #close menu to rerun selection_menu
                        return 3
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
            self.blit_selection_menu()
            event_listener()
            pygame.display.flip()
        return self.room_choice

    def build_selection_menu(self):
        self.size = self.window.size
        W, H = self.size
        Y_RATIO = self.Y_RATIO ; X_RATIO = self.X_RATIO ; X_STEP_RATIO = self.X_STEP_RATIO
        #image building
        self.bg_image.scale((W, H))
        for id,room in enumerate(self.rooms):
            room_img = Screen.room_imgs[room.name]
            room_img = pygame.transform.rotate(room_img, room.rotation*90)
            room_image = ImageFull(room_img)
            room_image.scale((int(W * 0.173), int(H * 0.173 * 16/9)))
            room_image.position = (W * (X_RATIO + X_STEP_RATIO*id), H * Y_RATIO)
            self.room_images[id]=(room_image)
        
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
        font = pygame.font.Font(None, int(H * 0.05))
        self.dice_text = font.render(str(self.dice_count), True, (255, 255, 255))
    
    def blit_selection_menu(self):
        W, H = self.size
        Y_RATIO = self.Y_RATIO ; X_RATIO = self.X_RATIO ; X_STEP_RATIO = self.X_STEP_RATIO
        buffer = self.buffer
        self.mainscreen.blit() #draw mainscreen
        buffer.blit(self.dark_overlay, (0, 0))
        buffer.blit(self.bg_image.scaled, (0, 0))
        for room_image in self.room_images:
            room_image.blit(buffer)
        #dice display
        self.dice_image.blit(buffer)
        buffer.blit(self.dice_text, self.dice_count_position)
        #white rectangle : recalculate position (and size for dice) if move
        if self.room_choice != 3:
            id = self.room_choice
            self.rect = pygame.Rect(W * (X_RATIO + X_STEP_RATIO*id), H * Y_RATIO, int(W * 0.174), int(W * 0.174))
        else:
            self.rect = pygame.Rect(W * 0.87, H * 0.2, int(W * 0.04), int(W * 0.04))
        pygame.draw.rect(buffer, (255, 255, 255), self.rect, width=4)
    
    def refresh(self):
        self.mainscreen.build()
        self.build_selection_menu(self.room_names)
        self.blit_selection_menu()

