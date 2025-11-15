"""Main game screen UI.

This module provides the MainScreen class which displays the main gameplay
interface, including the player's current room, inventory (consumables and
permanents), map grid, and door status (lock level) indicators.
"""

import pygame

from .window import Screen
from .image import ImageSimple, ImageReapeated
from .grids import Consumable_grid, door, Permanent_grid, Map_grid


class MainScreen(Screen):
    """Display the main gameplay screen with player inventory, map, and room status.
    
    Manages the display of:
        - Background image and consumable inventory (sidebar)
        - Equipped permanent items grid
        - Current room display and message
        - Game world map with room positions
        - Door and lock status indicator
    
    The screen provides methods to update individual components (consumables,
    permanents, map, player position, current room) to support incremental
    screen updates without full redraws.
    
    Attributes:
        SIZE_CURRENT_ROOM (float): Scale of current room image (relative to width).
        CURRENT_ROOM_POSITION (tuple): Position of current room display (0-1 relative).
        DOOR_POSITION (tuple): Position of door/lock status display (0-1 relative).
        MSG_SIZE (float): Message text size relative to FONT_SIZE.
        player (Player): Reference to the player object for rendering inventory.
        consumable_grid (Consumable_grid): Grid helper for consumable items.
        permanent_grid (Permanent_grid): Grid helper for permanent items.
        map_grid (Map_grid): Grid helper for the game world map.
    """
    SIZE_CURRENT_ROOM = 0.1823
    CURRENT_ROOM_POSITION = (0.3645,0.177)
    CURRENT_ROOM_MSG_SIZE = 0.7     #relative to FONT_SIZE
    CURRENT_ROOM_MSG_POSITION = (0.665,0.805)  #center of text
    DOOR_POSITION = (0.38,0.762)
    DOOR_SIZE = 0.09
    KEY_SIZE = DOOR_SIZE / 2
    #screen print
    MSG_SIZE = 0.95     #relative to FONT_SIZE
    MSG_POSITION = (0.727,0.22)    #center_position

    def __init__(self, player):
        """Initialize the main screen with the given player.
        
        Sets up all display grids (consumables, permanents, map) and prepares
        images for the current room, door status, and keys (representing the lock level).
        
        Args:
            player (Player): The player object to display on the main screen.
        
        Returns:
            None
        """
        Screen.__init__(self)
        self.buffer = Screen.window.buffer
        self.player = player
        #import images from loadscreen
        self.bg_image = ImageSimple(Screen.main_bg_img)
        #grids
        Screen.consumable_grid = Consumable_grid()
        self.permanent_grid = Permanent_grid()
        self.map_grid = Map_grid()
        self.closed_door_image = ImageSimple(Screen.closed_door_img)
        self.opened_door_image = ImageSimple(Screen.opened_door_img)
        self.key_image = ImageReapeated(Screen.consumable_imgs['key'])
        self.key_image.positions = [None]*3
        #display
        self.update()

    def build(self):
        """Build and scale all visual elements for the main screen.
        
        Prepares fonts, grid layouts, background, items, map, door status,
        and current room display based on current window size. This method
        recalculates all relative positions and scales all cached surfaces.
        
        Called during initialization and after window resize events.
        
        Returns:
            None
        """
        self.size = self.window.size
        w,h = self.size
        f = self.FONT_SIZE
        #set fonts
        txt_size = f * self.MSG_SIZE
        self.msg = pygame.font.SysFont(self.FONT, int(h * txt_size))
        self.msg.italic = True
        txt_size = f * self.CURRENT_ROOM_MSG_SIZE
        self.room_msg_font = pygame.font.SysFont(self.FONT, int(h * txt_size))
        self.set_all_relatives()
        self.build_bg_screen()
        self.build_items()
        self.map_grid.build_rooms(self.player)
        door.build(self.player.position)
        self.build_current_room()
        self.build_door_status()

    def blit(self):
        """Render all screen elements to the buffer.
        
        Blits background, items, map, door, and status elements to the
        internal buffer in the correct layering order.
        
        Returns:
            None
        """
        self.blit_bg_screen()
        self.blit_items() 
        self.map_grid.blit_rooms(self.buffer)
        door.draw(self.buffer)
        self.blit_status()

    def print(self, msg):
        """Render and display a message at the message position.
        
        Args:
            msg (str): Message text to display.
        """
        txt = self.msg.render(msg, True, (255, 255, 255))
        X, Y = self.MSG_POSITION ; w, h = self.size ; txt_w, txt_h = txt.get_size()
        position = (X*w - txt_w/2, Y*h + txt_h/2 )
        self.buffer.blit(txt, position)
        pygame.display.flip()

    
## updates
    def set_all_relatives(self):
        """Recalculate all grid coordinates relative to current window size.
        
        Called when the window is resized to update all layout parameters.
        """
        W, H = self.size
        Map_grid.set_grid(W,H)
        Consumable_grid.set_grid(W,H)
        Permanent_grid.set_grid(W,H)

    def update_consumables(self):
        """Rebuild and redisplay the consumables grid.
        
        Called when the player's consumable inventory changes.
        """
        self.build_items()
        self.blit()

    def update_permanents(self):
        """Rebuild and redisplay the permanents grid.
        
        Called when the player's equipped permanent items change.
        """
        self.blit_items()
        self.blit() # overkill if we cannot lose a permanent object

    def update_map(self):
        """Rebuild and redisplay the map grid.
        
        Called when the player's discovered rooms change.
        """
        self.map_grid.build_rooms(self.player)
        self.blit() # overkill if we cannot remove a room

    def update_player_position(self):
        """Update the display when the player moves to a new room.
        
        Updates door status, current room display, and map representation.
        """
        door.build(self.player.position)
        self.build_current_room()
        self.update_map()

    def update_current_room(self):
        """Rebuild and redisplay the current room display.
        
        Called when the current room's message or other properties change.
        """
        self.build_current_room()
        self.blit()


## builds, blits
    def build_bg_screen(self):
        """Build the background screen and consumable grid images.
        
        Background is invariant (does not change when items update), so scaling
        is cached here to avoid redundant calculations.
        
        Returns:
            None
        """
        W, H = self.size
        #back ground image
        self.bg_image.smoothscale((W, H))
        self.bg_image.position = (0,0)

        #scale all consumable images
        self.consumable_grid.scale_images()

    def blit_bg_screen(self):
        """Blit background image and consumable item images to buffer.
        
        Returns:
            None
        """
        buffer = self.buffer
        #back ground image
        self.bg_image.blit(buffer)
        #consumable images
        self.consumable_grid.blit_images(buffer)

    def build_items(self):
        """Build consumable counts and permanent item grid images.
        
        Returns:
            None
        """
        #consumable cpt 
        self.consumable_grid.build_text(self.player)
        #permanent objects
        self.permanent_grid.scale_images()

    def blit_items(self):
        """Blit consumable count texts and permanent item images to buffer.
        
        Returns:
            None
        """
        buffer = self.buffer
        #consumable cpt 
        self.consumable_grid.blit_text(buffer)
        #permanents
        self.permanent_grid.blit_images(buffer,self.player)

    def build_current_room(self):
        """Build the current room image and message display.
        
        Prepares the scaled room image and renders the room's entry message.
        
        Returns:
            None
        """
        w,h = self.size
        #build current room
        SIZE = self.SIZE_CURRENT_ROOM
        X,Y = self.CURRENT_ROOM_POSITION
        current_room_image = ImageSimple(Screen.room_imgs[self.player.current_room.name])
        current_room_image.smoothscale((SIZE * w, SIZE * h * 16/9))
        current_room_image.position = (X * w, Y * h)
        self.current_room_image = current_room_image
        #build enter_message
        X,Y = self.CURRENT_ROOM_MSG_POSITION
        current_room_txt = self.player.current_room.message
        if current_room_txt is not None:
            current_room_txt = self.room_msg_font.render(str(current_room_txt), True, (255, 255, 255))
            txt_w,txt_h = current_room_txt.get_size()
            self.current_room_txt_position = (X*w - txt_w/2, Y*h - txt_h/2)
        self.current_room_txt = current_room_txt

    def build_door_status(self):
        """Build opened/closed door images and key indicator images (representing lock levels).
        
        Prepares door and key images at correct positions for 0, 1, or 2 keys displayed (lock levels).
        
        Returns:
            None
        """
        w,h = self.size
        # build all door_status images
        DOOR_X,DOOR_Y = self.DOOR_POSITION; DOOR_SIZE = self.DOOR_SIZE; KEY_SIZE = self.KEY_SIZE
        #opened_door
        image = self.opened_door_image
        image.smoothscale((DOOR_SIZE * w, DOOR_SIZE * h * 16/9))
        image.position = (DOOR_X * w, DOOR_Y * h)
        self.opened_door_image = image
        #closed door
        image = self.closed_door_image
        image.smoothscale((DOOR_SIZE * w, DOOR_SIZE * h * 16/9))
        image.position = (DOOR_X * w, DOOR_Y * h)
        self.closed_door_image = image
        #key_0 image
        image = self.key_image
        offset = DOOR_SIZE/2 - KEY_SIZE/2
        image.scale((KEY_SIZE * w, KEY_SIZE * h * 16/9))
        image.positions[0] = ((DOOR_X + offset) * w,(DOOR_Y + offset*16/9) * h)
        #key1-2
        offset_y1 = offset - DOOR_SIZE/6
        offset_y2 = offset + DOOR_SIZE/6
        image.positions[1] = ((DOOR_X + offset) * w,(DOOR_Y + offset_y1*16/9) * h)
        image.positions[2] = ((DOOR_X + offset) * w,(DOOR_Y + offset_y2*16/9) * h)
        self.key_image = image

    def blit_status(self):
        """Blit current room, door status, and key indicators to buffer.
        
        Displays the appropriate door image (open/closed/locked) with
        the correct number of key indicators based on door_status.
        
        Returns:
            None
        """
        buffer = self.buffer
        #blit current room
        self.current_room_image.blit(buffer)
        if self.current_room_txt is not None:
            buffer.blit(self.current_room_txt,self.current_room_txt_position)
        # blit current doom_status
        door_status = self.player.door_status
        if door_status == 0 :   #wall
            return
        elif door_status == -1 :    #opened door
            self.opened_door_image.blit(buffer)
        elif door_status > 0 :      #closed door
            self.closed_door_image.blit(buffer)
            if door_status == 2 :   #locked1 door
                self.key_image.blit_single(buffer,0)
            elif door_status == 3:  #locked2 door
                self.key_image.blit_single(buffer,1)
                self.key_image.blit_single(buffer,2)