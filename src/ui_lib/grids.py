"""Grid helpers for drawing game items and map on UI screens.

This module provides grid layout classes that manage the positioning and
blitting of inventory items (consumables, permanents) and rooms on the map
using proportional offsets relative to screen size. Classes include:

- `Consumable_grid`: Displays inventory consumables in a vertical list with counts.
- `Permanent_grid`: Displays equipped permanent items in a 5-column grid layout.
- `Map_grid`: Displays the game world rooms with rotation handling.
- `door`: Helper class to build and draw door overlays on the map.

Each grid class uses class methods to set sizing/positioning parameters based
on screen dimensions (W, H), and instance methods to scale, blit, and render.
"""

import pygame
from .image import ImageSimple, ImageRoom
from .window import Screen
import database


class Consumable_grid:
    """Display consumable items in a vertical list with current inventory counts.
    
    This class manages a vertical grid of consumable items (coins, dice, etc.)
    displayed in a sidebar position, with text counts updated from the player's
    current inventory. All layout is computed using proportional offsets
    relative to screen dimensions.
    
    Methods:
        scale_images() -> None: Scale all consumable images.
        build_text(player) -> None: Render inventory count texts.
        blit_images(buffer) -> None: Blit item images to surface.
        blit_text(buffer) -> None: Blit count texts to surface.
        set_grid(w, h) -> None: Compute layout from screen dimensions.
    """
    TEXT_COLOR = (255, 255, 255)
    POSITION = (0.91, 0.13)         #relative to screen.size
    TXT_OFFSET = (0.03, 0.01)
    STEP = 0.046                    #relative to screen.size.h
    SIZE_TEXT = 0.045

    def __init__(self):
        """Initialize consumables grid by loading all consumable images from Screen."""
        self.names = []
        self.images = []
        imgs = Screen.consumable_imgs
        for name in database.consumables:  # in order set in database for display
            self.names.append(name)
            self.images.append(ImageSimple(imgs[name]))
        self.texts = [None]*len(self.names)
    
    def render_txt(self,font,msg): #unused
        """Render a single text message (utility method).
        (actally unused anymore, might get cleaned later)
        
        Args:
            font (pygame.font.Font): Font to use for rendering.
            msg (str): Message to render.
        """
        self.txt = font.render(msg, True, self.TEXT_COLOR)
    
    def scale_images(self):
        """Scale all consumable images to grid size and set positions.
        
        Returns:
            None
        """
        for id,image in enumerate(self.images):
            image.scale(self.consumable_size)
            image.position = self.get_position_img(id)

    def build_text(self,player):
        """Render inventory count texts for all consumables.
        
        Args:
            player (Player): Player object containing current inventory counts.
        
        Returns:
            None
        """
        self.font = pygame.font.Font(None, self.size_text)
        #consumable cpt 
        inventory_consumables = player.inventory.consumables
        font = self.font
        for id,name in enumerate(self.names):
            msg = str(inventory_consumables[name])
            self.texts[id] = font.render(msg, True, self.TEXT_COLOR)

    def blit_images(self,buffer):
        """Blit all consumable item images to the buffer.
        
        Args:
            buffer (pygame.Surface): Destination surface.
        
        Returns:
            None
        """
        for image in self.images:
            image.blit(buffer)

    def blit_text(self,buffer):
        """Blit all inventory count texts to the buffer.
        
        Args:
            buffer (pygame.Surface): Destination surface.
        
        Returns:
            None
        """
        for id,text in enumerate(self.texts):
            buffer.blit(text, self.get_position_txt(id))

    @classmethod
    def set_grid(cls,w,h):
        """Compute and cache grid layout parameters from screen dimensions.
        
        Args:
            w (int): Screen width in pixels.
            h (int): Screen height in pixels.
        
        Returns:
            None
        """
        X,Y = cls.POSITION
        TXT_X, TXT_Y = cls.TXT_OFFSET
        cls.x =  w * X                       #absolute position of consumables (upper left corner)
        cls.y = h * Y
        cls.txt_r_x = w * TXT_X                 #relative position of text from each row
        cls.txt_r_y = h * TXT_Y
        cls.step_y = h * cls.STEP                  #relative y position of each row from the previous one
        cls.consumable_size = (h//22,h//22)
        cls.size_text = int(cls.SIZE_TEXT * h)

    @classmethod
    def get_position_img(cls,rank):
        """Return the screen position of a consumable image by rank.
        
        Args:
            rank (int): 0-based index in the consumable list.
            
        Returns:
            tuple[float, float]: (x, y) position in pixels.
        """
        return (cls.x,
                cls.y + cls.step_y * rank)
    
    @classmethod
    def get_position_txt(cls,rank):
        """Return the screen position of a consumable count text by rank.
        
        Args:
            rank (int): 0-based index in the consumable list.
            
        Returns:
            tuple[float, float]: (x, y) position in pixels.
        """
        return (cls.x + cls.txt_r_x, 
                cls.y + cls.step_y * rank + cls.txt_r_y)
    



class Permanent_grid:
    """Display equipped permanent items in a 5-column grid layout.
    
    Permanent items (hammer, lockpick_kit, etc.) are displayed in a grid that fills
    left-to-right, top-to-bottom, skipping the top-right corner position.
    """

    def __init__(self):
        """Initialize permanent items grid by loading all permanent item images."""
        self.images = {}
        for name,image in Screen.permanant_imgs.items():
            self.images[name] = ImageSimple(image)   # no preset order

    def scale_images(self):
        """Scale all permanent item images to grid size.
        
        Returns:
            None
        """
        for image in self.images.values() :
            image.scale(self.perm_size)

    def blit_images(self,buffer,player):
        """Blit all equipped permanent items to the buffer.
        
        Args:
            buffer (pygame.Surface): Destination surface.
            player (Player): Player object with equipped permanents inventory.
        
        Returns:
            None
        """
        inv_permanents = player.inventory.permanents
        for id,name in enumerate(inv_permanents):
            buffer.blit(self.images[name].scaled, self.get_position_img(id))

    @classmethod
    def set_grid(cls,W,H):
        """Compute and cache grid layout parameters from screen dimensions.
        
        Args:
            W (int): Screen width in pixels.
            H (int): Screen height in pixels.
        """
        cls.x = W * 0.483                # absolute position
        cls.y = H * 0.45
        cls.step_x = W * 0.095 
        cls.step_y = H * 0.10
        cls.perm_size = (W//11, H//11)

    @classmethod
    def get_position_img(cls,rank):
        """Return the screen position of a permanent item by rank.
        
        Items fill left-to-right, then top-to-bottom, skipping the first position.
        
        Args:
            rank (int): 0-based index in the equipped permanents list.
            
        Returns:
            tuple[float, float]: (x, y) position in pixels.
        """
        rank = rank + 1                     # top_right corner unavailable
        x = (rank % 5) * cls.step_x + cls.x
        y = (rank // 5) * cls.step_y + cls.y
        #if rank == 1 : print(x,y)
        return x,y

class Map_grid:
    """Display the player's game world map with room positions and rotations.
    
    Manages the grid of rooms from the player's map, handling multiple rooms
    with the same image but different rotations.
    """

    def __init__(self):
        self.room_images = {}
    
    def build_rooms(self,player):
        """Build the room image cache from the player's current map.
        
        Reuses room images where the same room appears multiple times at different
        rotations, caching only unique room types.
        
        Args:
            player (Player): Player object containing the current game map.
        
        Returns:
            None
        """
        self.room_images = {}
        for col,col_rooms in enumerate(player.map.rooms):
            for row,room in enumerate(col_rooms):
                if room is not None :
                    name = room.name
                    if name not in self.room_images :
                        room_image = ImageRoom(Screen.room_imgs[name])  #store only rooms in map
                        room_image.scale(self.room_size)
                        room_image.positions.append((col,row,room.rotation))
                        self.room_images[name] = room_image
                    else:
                        self.room_images[name].positions.append((col,row,room.rotation))
    
    def blit_rooms(self,buffer):
        """Blit all rooms at their positions with correct rotations.
        
        Args:
            buffer (pygame.Surface): Destination surface.
        
        Returns:
            None
        """
        for room_image in self.room_images.values() :
            for position in room_image.positions :
                col,row,rot = position
                buffer.blit(room_image.scaled[rot], Map_grid.get_position_case(col,row))

    @classmethod
    def set_grid(cls,W,H):
        """Compute and cache map grid layout parameters from screen dimensions.
        
        Args:
            W (int): Screen width in pixels.
            H (int): Screen height in pixels.
        """
        cls.step_y = H * 0.0965 #0.0959
        cls.step_x = W * 0.054
        cls.base_x = W * 0.0615 #0.1695 # left of map_grid
        cls.base_y = H * 0.837  # bottom (up_corner) of map_grid
        #room size for rotations 0 and 2 (invert h and w for 1 and 3)
        cls.room_size = (int(W * 0.0547), int(H * 0.0547 * 16/9))   #0.0540

    @classmethod
    def get_position_case(cls,col,row):
        """Return the screen position of a map cell.
        
        Args:
            col (int): Column index in the map grid.
            row (int): Row index in the map grid.
            
        Returns:
            tuple[float, float]: (x, y) position in pixels (upper-left corner of the cell).
        """
        x = cls.base_x + col * cls.step_x   #left of case
        y = cls.base_y - row * cls.step_y   #top of case
        return x,y

class door:
    """Helper class to build and draw door overlays on map cells.
    
    Doors connect adjacent rooms and are drawn as rectangles positioned and
    oriented based on the door's rotation relative to the cell.
    """

    #Parameters :
    LENGTH = 40/100         # in step %
    THICKNESS = 6/100       # in step %

    @classmethod
    def build(cls,position):
        """Build a door rectangle for a given map cell position and rotation.
        
        Args:
            position (tuple): (col, row, rot) where rot is 0-3 for 0/90/180/270°.
        
        Returns:
            None
        """
        (col,row,rot) = position
        step_x, step_y = Map_grid.step_x, Map_grid.step_y
        length, thickness = cls.LENGTH, cls.THICKNESS
        x,y = Map_grid.get_position_case(col,row)

        r = 1 - rot // 2
        if rot%2 == 0 : # if pair (0:bot or 2:top)
            length = int(length * step_x)
            thickness = int(thickness * step_y)
            x = x + (step_x - length)//2    #centered
            w = length
            y = y + (step_y - thickness)*r
            h = thickness
        else:
            length = int(length * step_y)
            thickness = int(thickness * step_x)
            y = y + (step_y - length)//2    #centered
            h = length
            x = x + (step_x - thickness)*r
            w = thickness
        cls.door =  pygame.Rect(x,y,w,h)

    @classmethod
    def draw(cls,screen):
        """Draw the door rectangle on the given screen.
        
        Args:
            screen (pygame.Surface): Destination surface.
        
        Returns:
            None
        """
        COLOR = (255,255,255)
        pygame.draw.rect(screen,COLOR,cls.door)