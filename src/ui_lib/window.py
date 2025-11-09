import pygame
from .event_handler import EventHandler

class Window :
    WINDOW_RATIO = (16,9)
    default_window_size = (1920,1080)

    def __init__(self,UI):
        self.ui = UI
        #window size
        self.desk_W, self.desk_H = pygame.display.get_desktop_sizes()[0]    #import display_size
        W, H = self.window_try_size(self.default_window_size)
        self.size = W,H
        #window creation
        pygame.display.set_caption("Blue prince 2D")
        blueprince_icon = pygame.image.load("../images/blueprince_icon.jpeg")
        pygame.display.set_icon(blueprince_icon)
        self.buffer = pygame.display.set_mode(self.size,pygame.HIDDEN) #cannot convert() before set_mode()
        Screen.window = self
        
    def show_window(self):
        self.buffer = pygame.display.set_mode(self.size,pygame.RESIZABLE)
    
    def set_window_size(self,W,H):
        self.size = W,H

    def window_try_size(self,window_size):
        W,H = window_size
        #if default_window_size > display_size
        if W > self.desk_W or H > self.desk_H :
            (W,H) = self.maximize_window_with_ratio(self.desk_W,self.desk_H, W, H)
        #set window_size
        return (W,H)

    def maximize_window_with_ratio(self,desk_w,desk_h, W, H):
        #maximize window to biggest size inferior to current, keeping window_ratio
        ratio_W, ratio_H = self.WINDOW_RATIO
        while W > desk_w or H > desk_h :
            W -= ratio_W ; H -= ratio_H
        return (W,H)
    

class Screen :  #abstract
    window = None #set by window
    FONT_SIZE = 0.035
    TXT_POSITION = (0.5,0.91)    #center_position
    FONT = 'Arial'
    def __init__(self):
        self.size = Screen.window.size
        self.buffer = Screen.window.buffer
        self.event_handler = EventHandler
        _,h = self.size
        self.font = pygame.font.SysFont(self.FONT, int(h * self.FONT_SIZE))

    def screen_print(self,msg):
        txt = self.font.render(msg, True, (255, 255, 255))
        X, Y = self.TXT_POSITION ; w, h = self.size ; txt_w, txt_h = txt.get_size()
        position = (X*w - txt_w/2, Y*h + txt_h/2 )
        self.buffer.blit(txt, position)

    def update(self):
        self.build()
        self.blit()

    def buid(self):
        pass
    def blit(self):
        pass

    #loaded raw images
    consumable_imgs = {}
    permanant_imgs = {}
    room_imgs = {}
    bg_color_images = {}
