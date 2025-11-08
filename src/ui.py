import pygame

from ui_lib.window import Window
from ui_lib.load_screen import LoadScreen
from ui_lib.main_screen import MainScreen

class UI :
    fps = 60

    @classmethod
    def ini(cls):                  #initialise the class
        cls.clock = pygame.time.Clock()
        cls.window = Window(cls)      #set window size, font size, create window
        cls.screen = LoadScreen()   #loads ressources for load_screen, show window, show screen
        cls.screen.load_images()    #pseudo-async : (event_listener loop)
        return cls

    @classmethod
    def mainScreen(cls,player):
        cls.screen = MainScreen(player)


    @staticmethod
    def quit_game():
        pygame.quit()
        raise SystemExit() #or sys.exit()

    @classmethod
    def event_listener(cls):
        event_handler = cls.screen.event_handler
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                UI.quit_game()
            elif event_type == pygame.WINDOWRESIZED or event_type == pygame.WINDOWSIZECHANGED:
                cls.window.set_window_size(event.x,event.y)
                cls.screen.refresh()
            elif event_type == pygame.KEYDOWN:
                event_key = event.key
                if event_key == pygame.K_ESCAPE:
                    event_handler.escape()
                elif event_key == pygame.K_SPACE:
                    event_handler.space()
                elif event_key == pygame.K_RETURN:
                    event_handler.enter()
                elif event_key == pygame.K_BACKSPACE:
                    event_handler.back()
                elif event_key == pygame.K_z or event_key == pygame.K_w or event_key == pygame.K_UP :
                    event_handler.up()
                elif event_key == pygame.K_s or event_key == pygame.K_DOWN:
                    event_handler.down()
                elif event_key == pygame.K_q or event_key == pygame.K_a or event_key == pygame.K_LEFT:
                    event_handler.left()
                elif event_key == pygame.K_d or event_key == pygame.K_RIGHT:
                    event_handler.right()



