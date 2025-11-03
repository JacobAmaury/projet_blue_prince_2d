import pygame

from ui_lib.display import Display
from ui_lib.map_grid import door

class UI :
    #UI class must define all the Rect boxes needed for event_handling (mouse boxes)

    fps = 60

    @classmethod
    def ini(cls):                  #initialise the class
        cls.display = Display()      #set window size, font size, loads load_screen ressources
        cls.display.create_window()
        #create and load display
        cls.display.loadScreen.convert_loaded()
        cls.display.build_and_blit_loadScreen()
        pygame.display.flip()   #blit before loading ressources
        #set as current display for resising
        cls.refresh_current_display = cls.display.build_and_blit_loadScreen
        #load game ressources
        cls.display.load_images(cls.event_listener)    #checks for events : pseudo-async
        cls.room_choice = 0
        return cls

    @classmethod
    def set_player(cls,player):
        cls.display.player = player     #todo : remove nav.player from display
        cls.player = player

    @classmethod
    def build_mainScreen(cls):
        cls.display.set_all_grids_mainScreen()
        cls.display.build_bg_screen()
        cls.display.build_items()
        cls.display.build_rooms()
        door.build(cls.player.map.door)

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
        door.build(cls.player.map.door)
        cls.update_map()

    @classmethod
    def selection_menu(cls, room_names):
        """
        Display a selection menu for choosing one of three rooms.
        Returns the name of the selected room, or None if cancelled.
        """
        display = cls.display
        screen = display.screen
        W, H = display.size


        bg_menu_path = "../images/background/selection_menu.png"
        menu_bg = pygame.image.load(bg_menu_path).convert_alpha()
        menu_bg = pygame.transform.smoothscale(menu_bg, (W, H))

        #image loading and scaling
        room_imgs = []
        for name in room_names:
            img = display.room_images[name].loaded
            scaled = pygame.transform.smoothscale(img, (int(W * 0.173), int(W * 0.16)))
            room_imgs.append((name, scaled))

        positions = [
            (W * 0.309, H * 0.172),
            (W * 0.496, H * 0.172),
            (W * 0.683, H * 0.172),
        ]

        selected_room = None
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls.quit_game()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False  #close menu without selection
                        selected_room = None



            #draw menu
            cls.blit_mainScreen()
            dark_overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 180))
            screen.blit(dark_overlay, (0, 0))
            screen.blit(menu_bg, (0, 0))

            for (_, img), (x, y) in zip(room_imgs, positions):
                screen.blit(img, (x, y))


            #dice display
            dice_img = display.consumable_images[-1].loaded  
            dice_scaled = pygame.transform.smoothscale(dice_img, (int(W * 0.04), int(W * 0.04)))
            dice_x, dice_y = W * 0.87, H * 0.2
            screen.blit(dice_scaled, (dice_x, dice_y))

            dice_count = cls.player.inventory.consumables["dice"]
            font = pygame.font.Font(None, int(H * 0.05))
            dice_text = font.render(str(dice_count), True, (255, 255, 255))
            screen.blit(dice_text, (dice_x + W * 0.05, dice_y + H * 0.005))

            pygame.display.flip()



        # redraw main screen
        cls.blit_mainScreen()
        pygame.display.flip()

        return selected_room


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

    @classmethod
    def quit_game(cls):
        pygame.quit()
        raise SystemExit() #or sys.exit()
    
## event_handlers for player inputs
# keyboard inputs
class event_handler :
    escape = UI.quit_game
    space = lambda: print('space')
    enter = lambda: print('enter') 
    back = lambda: print('back')
    up = lambda: print('up')
    down = lambda: print('down')
    left = lambda: print('left')
    right = lambda: print('right')
UI.event_handler = event_handler
