import pygame

from ui_lib.display import Display
from ui_lib.map_grid import door

class UI :
    #UI class must define all the Rect boxes needed for event_handling (mouse boxes)

    def __init__(self,nav):
        UI.display = Display()    #set window size, font size, loads load_screen ressources
        UI.display.create_window()
        #create and load display
        UI.display.loadScreen.convert_loaded()
        UI.display.build_and_blit_loadScreen()
        pygame.display.flip()   #blit before loading ressources
        #set as current display for resising
        UI.refresh_current_display = UI.display.build_and_blit_loadScreen
        #load game ressources
        UI.display.load_images(UI.event_listener)    #checks for events : pseudo-async
        UI.nav = nav

    @classmethod
    def build_mainScreen(cls):
        cls.display.set_all_grids_mainScreen()
        cls.display.build_bg_screen()
        cls.display.build_items()
        cls.display.build_rooms()
        door.build(cls.nav.map.door)

    @classmethod
    def blit_mainScreen(cls):
        cls.display.blit_bg_screen()
        cls.display.blit_items() 
        cls.display.blit_rooms()
        door.draw(cls.display.screen)

    @classmethod
    def build_and_blit_mainScreen(cls):
        cls.build_mainScreen()
        cls.blit_mainScreen()

    @classmethod
    def mainScreen(cls):
        cls.build_and_blit_mainScreen()
        #set as current screen for blitting
        cls.refresh_current_display = cls.build_and_blit_mainScreen

    @classmethod
    def update_consumables(cls):
        cls.display.build_items()
        cls.blit_mainScreen()

    @classmethod
    def update_permanents(cls):
        cls.display.blit_items()
        cls.blit_mainScreen() # overkill if we cannot lose a permanent object

    @classmethod
    def update_map(cls):
        cls.display.build_rooms()
        cls.blit_mainScreen() # overkill if we cannot remove a room

    @classmethod
    def update_door(cls):
        door.build(cls.nav.map.door)
        cls.update_map()

    @classmethod
    def selectionScreen(cls,prompt_msg,items):
        pass

    @classmethod
    def event_listener(cls):
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                UI.quit_game()
            elif event_type == pygame.WINDOWRESIZED or event_type == pygame.WINDOWSIZECHANGED:
                cls.display.size = event.x,event.y
                cls.refresh_current_display()
                pygame.display.flip()   #need to flip during loadScreen
            elif event_type == pygame.KEYDOWN:
                event_key = event.key
                if event_key == pygame.K_ESCAPE:
                    event_handler.escape()
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

    @classmethod
    def quit_game(cls):
        pygame.quit()
        raise SystemExit() #or sys.exit()
    
## event_handlers for player inputs
# keyboard inputs
class event_handler :
    escape = UI.quit_game
    enter = lambda: print('enter')
    back = lambda: print('back')
    up = lambda: print('up')
    down = lambda: print('down')
    left = lambda: print('left')
    right = lambda: print('right')
UI.event_handler = event_handler
