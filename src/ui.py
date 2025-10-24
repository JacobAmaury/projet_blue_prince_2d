import pygame

from ui_lib.display import Display
from ui_lib.map_grid import door
from navigation import Nav

class UI :
    #UI class must define all the Rect boxes for input_handler management (mouse boxes)

    def __init__(self):
        self.display = Display()    #set window size, font size, loads load_screen ressources
        self.display.create_window()
        #create and load display
        self.display.loadScreen.convert_loaded()
        self.display.build_and_blit_loadScreen()
        pygame.display.flip()   #blit before loading ressources
        #set as current display for resising
        self.refresh_current_display = self.display.build_and_blit_loadScreen
        #load game ressources
        self.display.load_images(self.event_listener)    #checks for events : pseudo-async
        #initialise Navigation (=game controller)
        self.nav = Nav(self)
        #start a new game
        self.nav.new_game()

    def build_mainScreen(self):
        self.display.set_all_grids_mainScreen()
        self.display.build_bg_screen()
        self.display.build_items()
        self.display.build_rooms()
        door.build(self.nav.map.door)

    def blit_mainScreen(self):
        self.display.blit_bg_screen()
        self.display.blit_items() 
        self.display.blit_rooms()
        door.draw(self.display.screen)

    def build_and_blit_mainScreen(self):
        self.build_mainScreen()
        self.blit_mainScreen()

    def mainScreen(self):
        self.build_and_blit_mainScreen()
        #set as current screen for blitting
        self.refresh_current_display = self.build_and_blit_mainScreen

    def update_consumables(self):
        self.display.build_items()
        self.blit_mainScreen()

    def update_permanents(self):
        self.display.blit_items()
        self.blit_mainScreen() # overkill if we cannot lose a permanent object

    def update_map(self):
        self.display.build_rooms()
        self.blit_mainScreen() # overkill if we cannot remove a room

    def update_door(self):
        door.build(self.nav.map.door)
        self.update_map()

    def selectionScreen_temp(self,prompt_msg,items):
        #temporary terminal function for selectionScreen
        print('Selection choice :')
        print(prompt_msg)
        for nb,i in enumerate(items):
            print(f'{nb}. ',i)

    def event_listener(self):
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                UI.quit_game()
            elif event_type == pygame.WINDOWRESIZED or event_type == pygame.WINDOWSIZECHANGED:
                self.display.size = event.x,event.y
                self.refresh_current_display()
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
