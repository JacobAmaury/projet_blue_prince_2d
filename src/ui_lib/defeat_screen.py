import pygame
from .image import ImageSimple
from .event_handler import EventHandler
from .window import Screen

class DefeatScreen(Screen):

    def __init__(self):
        Screen.__init__(self)

        # background
        self.bg_image = ImageSimple(Screen.defeat_img)

        self.update()

    def build(self):
        w, h = self.window.size

        # scale background
        self.bg_image.smoothscale((w, h))
        self.bg_image.position = (0, 0)

        # text
        font = pygame.font.SysFont("Arial", int(h * 0.07))
        self.text = font.render("Press ENTER to restart", True, (255, 255, 255))
        tw, th = self.text.get_size()
        self.text_pos = (w/2 - tw/2, h*0.8)

    def blit(self):
        self.bg_image.blit(self.buffer)
        self.buffer.blit(self.text, self.text_pos)

    def select(self):
        class MenuHandler(EventHandler):
            @staticmethod
            def enter():
                from navigation import Nav, NavHandler
                Nav.new_game()
                # back to the main screen
                Nav.ui.show_mainScreen(Nav.player, NavHandler)
                self.running = False

        self.event_handler = MenuHandler
        event_listener = self.window.ui.event_listener

        self.running = True
        while self.running:
            event_listener()
            pygame.display.flip()

