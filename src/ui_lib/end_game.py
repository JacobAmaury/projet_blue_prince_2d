import pygame
from .image import ImageSimple
from .event_handler import EventHandler
from .window import Screen

class EndScreen(Screen):
    TITLE_POSITION = (0.5,0.15) # bloc center
    TITLE_SIZE = 3   #relative to FONT_SIZE
    RED = (255, 0, 0)
    # BLOC_POSITION = (0.5,0.5) # bloc center
    # STEP = 0.02     #relative to screen.size.h
    # BLUE = (50,150,255)

    def __init__(self,title):
        Screen.__init__(self)
        self.title = title

        # background
        self.bg_image = ImageSimple(Screen.defeat_img)

        # update
        self.update()

    def build(self):
        w, h = self.window.size
        TITLE_X, TITLE_Y = self.TITLE_POSITION

        # scale background
        self.bg_image.smoothscale((w, h))
        self.bg_image.position = (0, 0)

        #title
        title_font = pygame.font.SysFont(self.FONT, int(h * self.TITLE_SIZE * self.FONT_SIZE))
        self.title_text = title_font.render(self.title, True, self.RED)
        tw, th = self.title_text.get_size()
        self.title_position = (TITLE_X*w - tw/2, TITLE_Y*h - th/2)

        # text
        font = pygame.font.SysFont("Arial", int(h * 0.07))
        self.text = font.render("Press ENTER to restart", True, (255, 255, 255))
        tw, th = self.text.get_size()
        self.text_pos = (w/2 - tw/2, h*0.8)

    def blit(self):
        buffer = self.buffer
        self.bg_image.blit(buffer)
        buffer.blit(self.text, self.text_pos)
        #title
        buffer.blit(self.title_text, self.title_position)

    def select(self):
        class MenuHandler(EventHandler):
            @staticmethod
            def enter():
                self.running = False

        self.event_handler = MenuHandler
        event_listener = self.window.ui.event_listener

        self.running = True
        while self.running:
            event_listener()
            pygame.display.flip()

