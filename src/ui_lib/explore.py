import pygame

from .image import ImageSimple
from .event_handler import EventHandler
from .window import Screen
from .grids import Consumable_grid


class Explore(Screen):
    
    H = 0.8 ; STEP = 0.15
    BLUE = (50,150,255)
    SIZE = 0.1 #w ratio
    TXT_OFFSET = (0.025,0.007)
    WHITE = (255,255,255)
    SIZE_TXT = 0.07
    PRINT_TXT_POSITION = (.5, .1)

    def __init__(self, items, color):
        Screen.__init__(self)
        items = items[:6]
        self.items = items
        self.length = len(items)
        length = self.length
        self.player = self.window.ui.player
        self.selected = 0
        #import images from loadscreen
        self.bg_image = Screen.bg_color_images[color]
        self.images = [None]*length
        self.counts = [None]*length
        self.txt_positions = [None]*length
        categories = {'consumable':Screen.consumable_imgs, 
                      'permanent':Screen.permanant_imgs,
                      'other':Screen.other_imgs}
        for id,(name,nb,category) in enumerate(items):
            self.images[id] = ImageSimple(categories[category][name])
            self.counts[id] = nb
        self.build()
        self.blit()

    def build(self):
        w, h = self.size
        #back ground image
        self.bg_image.smoothscale((w, h))
        self.bg_image.position = (0,0)
        ###
        #items
        self.count_font = pygame.font.SysFont('Arial', int(self.SIZE_TXT*h) )
        txt_positions = self.txt_positions
        off_x, off_y = self.TXT_OFFSET
        x_center = w/2 ; SIZE = self.SIZE ; H = self.H ; STEP = self.STEP
        step = STEP*w
        width = step*self.length
        x = x_center - width/2
        for id,image in enumerate(self.images):
            image.scale((SIZE*h, SIZE*h))
            xi = x + step*(id) + step/2
            wi = image.scaled.get_width()
            xi_c = xi-wi/2 ; yi = H*h
            image.position = (xi_c, yi)
            txt_positions[id]=((xi_c - off_x*w, yi + off_y*h))


    def blit(self):
        buffer = self.buffer
        #back ground image
        self.bg_image.blit(buffer)
        #consumable images
        self.consumable_grid.blit_images(buffer)
        #consumable cpt 
        self.consumable_grid.blit_text(buffer)
        ###
        selected = self.selected
        buffer = self.buffer
        #build selector
        txt_positions = self.txt_positions
        counts = self.counts ; white = self.WHITE ; blue = self.BLUE
        #blit rows
        for id,image in enumerate(self.images):
            image.blit(buffer)
            color = white if selected != id else blue
            buffer.blit(self.count_font.render(str(counts[id]),True, color), txt_positions[id])


    def print(self,msg):
        txt = self.font.render(msg, True, (255, 255, 255))
        X, Y = self.PRINT_TXT_POSITION ; w, h = self.size ; txt_w, txt_h = txt.get_size()
        position = (X*w - txt_w/2, Y*h + txt_h/2 )
        self.buffer.blit(txt, position)
        pygame.display.flip()

    def select(self):
        """
        Returns the rank, -1 if cancelled
        """ 
        # Why not just return index ?
        class MenuHandler(EventHandler):
            @staticmethod
            def escape() : 
                self.running=False
                self.selected = -1
            @staticmethod
            def left():
                self.selected = (self.selected - 1) % self.length
                self.blit()
            @staticmethod
            def right():
                self.selected = (self.selected + 1)  % self.length
                self.blit()
            @staticmethod
            def enter() : 
                self.running = False  #close menu with selection
            ##optionnal handlers : not in the game specifications (easier debugg), can be removed later
            @staticmethod
            def space():
                # take all
                self.running=False
                self.selected = self.length
            @staticmethod
            #cancel if go back or up
            def up():
                MenuHandler.escape()
            def down():
                MenuHandler.escape()
        self.event_handler = MenuHandler
        event_listener = self.window.ui.event_listener

        self.running = True
        while self.running:
            event_listener()
            pygame.display.flip()
        return self.selected
    

    def update(self):
        self.size = self.window.size
        w, h = self.size
        Consumable_grid.set_grid(w,h)
        #scale all consumable images
        self.consumable_grid.scale_images()
        #consumable cpt 
        self.consumable_grid.build_text(self.player)
        return super().update()