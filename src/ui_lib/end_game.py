import pygame
from .image import ImageSimple
from .event_handler import EventHandler
from .window import Screen

class EndScreen(Screen):
    #title
    TITLE_POSITION = (0.5,0.15) # bloc center
    TITLE_SIZE = 3   #relative to FONT_SIZE
    RED = (255, 0, 0)
    #selection bloc
    BLOC_POSITION = (0.5,0.8) # bloc center
    TEXT_SIZE = 2.5   #relative to FONT_SIZE
    STEP = 0.11     #relative to screen.size.h
    BLUE = (50,150,255)
    WHITE = (255, 255, 255)

    def __init__(self,title):
        Screen.__init__(self)
        self.title = title
        # background
        self.bg_image = ImageSimple(Screen.defeat_img)
        #selection bloc
        self.selected = 0
        self.choices = ['New game', 'Quit game']
        self.len = len(self.choices)
        # update
        self.update()

    def build(self):
        w, h = self.window.size
        self.size = w,h
        TITLE_X, TITLE_Y = self.TITLE_POSITION
        FONT = self.FONT ; FONT_SIZE = self.FONT_SIZE
        # scale background
        self.bg_image.smoothscale((w, h))
        self.bg_image.position = (0, 0)
        #title
        title_font = pygame.font.SysFont(FONT, int(h * self.TITLE_SIZE * FONT_SIZE))
        self.title_text = title_font.render(self.title, True, self.RED)
        tw, th = self.title_text.get_size()
        self.title_position = (TITLE_X*w - tw/2, TITLE_Y*h - th/2)
        # text choice
        self.text_size = int(h * self.TEXT_SIZE * FONT_SIZE)
        self.text_font = pygame.font.SysFont(FONT, self.text_size)

    def blit(self):
        w,h = self.size
        buffer = self.buffer
        self.bg_image.blit(buffer)
        # title
        buffer.blit(self.title_text, self.title_position)
        # text choice
        X,Y = self.BLOC_POSITION #center of bloc
        step = self.STEP * h
        y0 = Y*h - (self.text_size*self.len + step)//2
        for id,choice in enumerate(self.choices):
            color = self.BLUE if self.selected == id else self.WHITE
            text = self.text_font.render(choice, True, color)
            tw, _ = text.get_size()
            text_pos = (w*X - tw/2, y0 + step*id)
            buffer.blit(text, text_pos)

    def select(self):
        class MenuHandler(EventHandler):
            @staticmethod
            def enter():
                self.running = False
            @staticmethod
            def up():
                self.selected = (self.selected - 1) % self.len
                self.blit()
            @staticmethod
            def down():
                self.selected = (self.selected + 1)  % self.len
                self.blit()
            @staticmethod
            def space():
                MenuHandler.enter()


        self.event_handler = MenuHandler
        event_listener = self.window.ui.event_listener

        self.running = True
        while self.running:
            event_listener()
            pygame.display.flip()

        return self.selected

