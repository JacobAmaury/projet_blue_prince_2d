"""UI shop screen: displays products and handles selection/purchase UI.

This module provides the `Shop` screen class used by the main UI to
present available consumable products to the player. The screen renders
product names, prices and a coin icon, and exposes `select()` to run a
simple menu loop that returns the selected index (or -1 if cancelled).
"""

import pygame

from .image import ImageSimple
from .event_handler import EventHandler
from .window import Screen
from .grids import Consumable_grid


class Shop(Screen):
    """Screen used to show and choose products in the in-game shop.

    Displays a vertical list of purchasable items with their prices marked
    by coin icons. The player navigates (up/down) to select an item and
    confirms with enter. 
    
    Layout constants (all as ratios of window width/height):
        H1 (float): Vertical position of Shop screen header.
        X1 (float): Horizontal position of product names.
        X2 (float): Horizontal position of prices/coins.
        H2 (float): Vertical position of first product row.
        STEP (float): Vertical spacing between product rows.
        SIZE_COIN (float): Size of coin icon (ratio of height).
        X_COIN_OFFSET (float): Horizontal offset of coin from price text.
    
    Attributes:
        items (list): List of (name, price) tuples shown in the shop.
        len (int): Number of products (<= 9).
        player: Reference to the current player.
        selected (int): Currently highlighted product index.
        bg_image (ImageSimple): Background image wrapper.
        coin_image (ImageSimple): Coin icon image.
        consumable_grid (Consumable_grid): Grid helper for left-side inventory.
    """

    H1 = 0.2 ; X1 = 0.2 ; X2 = 0.62
    H2 = 0.3 ; STEP = 0.06
    WHITE = (255, 255, 255) ; BLUE = (50,150,255) ; YELLOW = (255, 255, 0)
    SIZE_COIN = 0.052   #h ratio
    X_COIN_OFFSET = 0.014

    def __init__(self, items):
        """Create a Shop screen showing up to 9 products.

        Args:
            items (iterable): sequence of (name, price) pairs to display.
        
        Returns:
            None
        """
        Screen.__init__(self)
        items = items[:9]
        self.items = items
        self.len = len(items)
        self.player = self.window.ui.player
        self.selected = 0
        # import images from loadscreen
        self.bg_image = Screen.shop
        self.coin_image = ImageSimple(Screen.consumable_imgs['coin'])
        self.update()

    def build(self):
        """Prepare rendering surfaces and scale images for the current window.

        This method is called when the screen needs to layout itself (for
        example after a window resize). It sets up fonts, scales the
        background and coin images, and prepares the consumable grid.
        
        Returns:
            None
        """
        self.size = self.window.size
        w, h = self.size
        # back ground image
        self.bg_image.smoothscale((w, h))
        self.bg_image.position = (0,0)
        # consumables
        Consumable_grid.set_grid(w,h)
        self.consumable_grid.scale_images()
        self.consumable_grid.build_text(self.player)
        # Title
        title_font = pygame.font.SysFont('Arial', int(0.07*h) )
        title = title_font.render('Welcome to the shop', True, self.YELLOW)
        self.title = title
        tw, th = title.get_size()
        self.title_position = (0.5*w - tw/2, 0.1*h - th/2)
        title2_font = pygame.font.SysFont('Arial', int(0.06*h) )
        WHITE = self.WHITE
        self.product_title = title2_font.render('Products :', True, WHITE)
        H = self.H1 ; X1 = self.X1 ; X2 = self.X2
        self.product_title_pos = (X1*w, H*h)
        self.price_title = title2_font.render('Price', True, WHITE)
        self.price_title_pos = (X2*w, H*h)
        self.product_font = pygame.font.SysFont('Arial', int(0.05*h) )
        # coin
        size = self.SIZE_COIN
        self.coin_image.scale((size*h, size*h))

    def update_products(self):
        """Render product name/price surfaces into `self.txt_products` and
        blit them to the internal buffer.

        The method updates highlight color based on the current
        `self.selected` index and draws the coin icon beside prices.
        
        Returns:
            None
        """
        w, h = self.size
        selected = self.selected; BLUE = self.BLUE; WHITE = self.WHITE
        # build rows
        product_font = self.product_font
        self.txt_products = []
        for id,(name,price) in enumerate(self.items):
            if selected != id : color = WHITE 
            else: color = BLUE
            self.txt_products.append((product_font.render(name,True, color),
                                      product_font.render(str(price),True, color)))
        # blit rows
        H = self.H2 ;  STEP = self.STEP ; X1 = self.X1 ; X2 = self.X2 ; x_coin_of = self.X_COIN_OFFSET
        of_x1 = self.product_title.get_width()/2 ; of_x2 = self.price_title.get_width()/2
        for id,txt_product in enumerate(self.txt_products):
            self.buffer.blit(txt_product[0], (X1*w + of_x1, (H + STEP*id)*h))
            ofx_txt2 = txt_product[1].get_width()/2
            x = X2*w + of_x2 ; y =  (H + STEP*id)*h
            self.buffer.blit(txt_product[1], (x - ofx_txt2, y))
            self.buffer.blit(self.coin_image.scaled, (x + x_coin_of*w, y))




    def blit(self):
        """Draw the full shop screen into the internal buffer.

        This composes background, consumable images and text, titles and
        the product list by delegating row rendering to
        `update_products()`.
        
        Returns:
            None
        """
        w, h = self.size
        buffer = self.buffer
        # back ground image
        self.bg_image.blit(buffer)
        # consumable images
        self.consumable_grid.blit_images(buffer)
        # consumable cpt 
        self.consumable_grid.blit_text(buffer)
        # titles
        self.buffer.blit(self.title,self.title_position)
        self.buffer.blit(self.product_title,self.product_title_pos)
        self.buffer.blit(self.price_title,self.price_title_pos)
        self.update_products()

    def select(self):
        """Run the shop menu loop and return the selected product index.

        The loop sets a temporary `MenuHandler` subclass of
        `EventHandler` to process navigation keys (up/down/enter/escape).
        It returns the selected index or -1 if the menu was cancelled.

        Returns:
            int: selected product index, or -1 if cancelled.
        """
        # Inner handler maps keys to menu actions. It uses the enclosing
        # instance's attributes (`self.selected`, `self.running`).
        class MenuHandler(EventHandler):
            @staticmethod
            def escape() : 
                self.running=False
                self.selected = -1
            @staticmethod
            def up():
                self.selected = (self.selected - 1) % self.len
                self.blit()
            @staticmethod
            def down():
                self.selected = (self.selected + 1)  % self.len
                self.blit()
            @staticmethod
            def enter() : 
                self.running = False  # close menu with selection
            # optional handlers: convenience for debugging; can be removed
            @staticmethod
            def space():
                MenuHandler.enter()
            @staticmethod
            # cancel if go left/right
            def right():
                MenuHandler.escape()
            def left():
                MenuHandler.escape()
        self.event_handler = MenuHandler
        event_listener = self.window.ui.event_listener

        self.running = True
        while self.running:
            event_listener()
            pygame.display.flip()
        return self.selected
    