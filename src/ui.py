import pygame


from display import Display
from navigation import Nav

class UI :
    #UI class must define all the Rect boxes for input_handler management (mouse boxes)

    def __init__(self):
        self.display = Display()    #set window size, font size

    def load(self):
        #create and load display
        self.display.load_loadScreen_images()
        self.display.create_window()
        self.display.build_and_blit_loadScreen()
        pygame.display.flip()   #blit before loading ressources
        #set as current display for resising
        self.refresh_current_display = self.display.build_and_blit_loadScreen

        #load game ressources
        self.display.load_images(self.event_handler)    #checks for events : pseudo-async

        #initialise Navigation (=game controller)
        self.nav = Nav(self)

        #start a new game
        self.nav.new_game()

    def build_mainScreen(self):
        self.display.build_bg_screen()
        self.display.build_items()
        self.display.build_rooms()

    def blit_mainScreen(self):
        self.display.blit_bg_screen()
        self.display.blit_items() 
        self.display.blit_rooms()

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
        self.blit_mainScreen() # useless if we cannot lose a permanent object

    def update_map(self):
        self.display.build_rooms()
        self.display.blit_rooms()

    def event_handler(self):
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                pygame.quit()
                raise SystemExit() #or sys.exit()
            
            elif event_type == pygame.WINDOWRESIZED or event_type == pygame.WINDOWSIZECHANGED:
                self.display.W,self.display.H = event.x,event.y
                self.refresh_current_display()
                pygame.display.flip()   #need to flip during loadScreen

            elif event_type == pygame.KEYDOWN:
                event_key = event.key
                if event_key == pygame.K_ESCAPE:
                    self.nav.input.escape()
                elif event_key == pygame.K_RETURN:
                    self.nav.input.enter()
                elif event_key == pygame.K_BACKSPACE:
                    self.nav.input.back()
                elif event_key == pygame.K_z or event_key == pygame.K_w or event_key == pygame.K_UP :
                    self.nav.input.up()
                elif event_key == pygame.K_s or event_key == pygame.K_DOWN:
                    self.nav.input.down()
                elif event_key == pygame.K_q or event_key == pygame.K_a or event_key == pygame.K_LEFT:
                    self.nav.input.left()
                elif event_key == pygame.K_d or event_key == pygame.K_RIGHT:
                    self.nav.input.right()


