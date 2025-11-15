"""Loading screen that initializes and displays the UI while loading game resources.

This module provides the LoadScreen class which shows a splash screen with
a background image and logo while asynchronously loading all game resources
(images for items, rooms, backgrounds, etc.) into class attributes of the
`Screen` helper. To remain responsive to user input during long IO operations,
the loading process calls `event_listener()` between resource batches.
"""

import pygame
import database

from .image import Image, ImageSimple
from .window import Screen

class LoadScreen(Screen):
    """Display this screen while loading all game resources asynchronously.
    
    Manages initial asset loading for the game, including background images,
    item graphics (consumables, permanents, others), room images, and UI elements
    (doors, menus). To keep the UI responsive during IO-bound loading, this
    class calls `event_listener()` between major batches of asset loads so
    the user can interact with the window (e.g., resize or close it) while
    resources are being loaded.
    
    The loaded images are stored in class attributes of `Screen` (e.g.,
    `Screen.consumable_imgs`, `Screen.room_imgs`) for use by all other screens.
    
    Attributes:
        bg_image (ImageSimple): The background image shown behind the logo.
        logo_image (ImageSimple): The Blue Prince logo displayed during loading.
        title (str): Message shown during loading (e.g., 'Loading game ...').
    """
    #convention : image = instance of Image, img = Surface

    def __init__(self):
        """Initialize the load screen and display the screen.
        
        Loads the background and logo images, makes the window visible, and
        prepares the screen for display. The window is initially hidden and
        is shown only when this constructor completes, allowing images to be
        converted to the display format before showing the window.
        
        Returns:
            None
        """
        Screen.__init__(self)
        #load images
        bg_path="../images/background/BluePrince_Start.jpg"
        logo_path="../images/Logo_Blue_Prince.png"
        Screen.bg_image = ImageSimple(Image.loadFull(bg_path))
        self.logo_image = ImageSimple(Image.loadTransparent(logo_path))
        #show window (was Hidden)
        self.window.show_window()
        self.update()

    def build(self):
        """Prepare the background and logo images for rendering.
        
        Scales the background to fill the window and the logo to 1/3 of the
        window size, positioned near the top-left corner.
        """
        buffer = self.window.buffer
        ##build_load_screen
        W,H = self.window.size
        self.size = W,H
        #images
        Screen.bg_image.smoothscale((W,H))
        Screen.bg_image.position = (0,0)
        self.logo_image.smoothscale((W//3, H//3))
        self.logo_image.position = (W//3 - self.logo_image.scaled.get_width()//2, H//20)

    def blit(self):
        """Render the load screen (background, logo, and 'Loading...' message).
        
        Blits the background and logo to the buffer and prints a 'Loading game...'
        message, then updates the display.
        """
        buffer = self.window.buffer
        ##blit_load_screen
        #images
        self.bg_image.blit(buffer)
        self.logo_image.blit(buffer)   
        #text (build and blit)
        self.print("Loading game ...")
        ##flip
        pygame.display.flip()
        



    def load_images(self):
        """Load all game resources asynchronously, polling events between batches.
        
        Loads images for backgrounds, items (consumables, permanents, others),
        rooms, doors, and UI elements. To remain responsive to user input during
        this IO-intensive operation, `event_listener()` is called between major
        batches so the window can be resized or closed gracefully.
        
        All loaded images are stored in class attributes on the `Screen` class
        (e.g., `Screen.consumable_imgs`, `Screen.room_imgs`, `Screen.bg_color_images`)
        so they are accessible to other screen classes throughout the game.
        """
        event_listener = self.window.ui.event_listener
        #background image mainscreen
        path = "../images/background/bg_image.png"
        Screen.main_bg_img = Image.loadFull(path)

        #defeat screen
        Screen.defeat_img = Image.loadFull("../images/background/defeat.png")

        #shop bg
        path = "../images/background/shop.jpg"
        Screen.shop = ImageSimple(Image.loadFull(path))
        event_listener() #loading may be long : handles user input

        #explore bg
        colors = ['violet']
        for color in colors:
            path = f"../images/background/{color}_room.jpeg"
            Screen.bg_color_images[color] = ImageSimple(Image.loadFull(path))
        colors = ['blue','orange', 'red', 'green']
        for color in colors:
            path = f"../images/background/{color}_room.jpg"
            Screen.bg_color_images[color] = ImageSimple(Image.loadFull(path))
            event_listener() #loading may be long : handles user input

        #consumables
        for name in database.consumables :
            path = "../images/items/consumables/"+ name +"_icon.png"
            Screen.consumable_imgs[name] = Image.loadTransparent(path)
        event_listener() #loading may be long : handles user input

        #permanent objects
        for name in database.permanents:
            path = "../images/items/permanents/"+ name +"_White_Icon.png"
            Screen.permanant_imgs[name] = Image.loadTransparent(path)
        event_listener() #loading may be long : handles user input

        #other objects
        for name in database.others:
            path = f"../images/items/others/{name}.png"
            Screen.other_imgs[name] = Image.loadTransparent(path)
        event_listener() #loading may be long : handles user input

        #rooms : import all rooms by names from Rooms_db.rooms
        for name,room_data in database.rooms.items():
            path = "../images/rooms/"+ room_data['color'] +'/'+ name +'.png'
            Screen.room_imgs[name] = Image.loadFull(path)
            event_listener() #loading may be long : handles user input

        #image menu
        bg_menu_path = "../images/background/selection_menu.png"
        Screen.selectionmenu_bg_img = Image.loadTransparent(bg_menu_path)

        #door status
        path = "../images/items/doors/closed_door.png"
        Screen.closed_door_img = Image.loadTransparent(path)
        path = "../images/items/doors/opened_door.png"
        Screen.opened_door_img = Image.loadTransparent(path)