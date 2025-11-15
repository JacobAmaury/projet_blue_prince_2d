import pygame

from ui_lib.window import Window
from ui_lib.load_screen import LoadScreen
from ui_lib.main_screen import MainScreen
from ui_lib.select_room import SelectRoom
from ui_lib.shop import Shop
from ui_lib.explore import Explore
from ui_lib.end_game import EndScreen


class UI:
    """Main UserInterface controller class for managing all game screens and user interactions.
    
    This class manages all user interfaces, including initialization,
    screen management, and event handling across different game states
    (main screen, shop, room selection, exploration, etc.).
    
    Attributes:
        fps (int): Frames per second for the game loop (default: 60).
        clock (pygame.time.Clock): Clock object for controlling frame rate.
        window (Window): Main game window object.
        screen (pygame.Surface): Current screen being displayed.
        player (Player): Current player object.
    """
    fps = 60

    @classmethod
    def ini(cls):
        """Initialize the UI system.
        
        Sets up the pygame clock for frame rate control and creates
        the window with appropriate size.
        
        Returns:
            UI: The UI class for method chaining. (to avoid circular import issues)
        """
        cls.clock = pygame.time.Clock()
        cls.window = Window(cls)  # set window size, create window
        return cls
    
    @classmethod
    def loadgame(cls):
        """Load and display the loading screen.
        
        Initializes the LoadScreen and loads all game resources asynchronously with user input
        through an event listener loop.
        """
        cls.screen = LoadScreen()  # loads resources for load_screen, show window, show screen
        cls.screen.load_images()   # pseudo-async: (event_listener loop)
    
    @classmethod
    def show_mainScreen(cls, player, event_handler):
        """Display the main game screen.
        
        Args:
            player (Player): The player object to display on the main screen.
            event_handler: The EventHandler object defining all handlers to process user input.
        """
        cls.player = player
        cls.screen = MainScreen(player)
        cls.screen.event_handler = event_handler
 
    #private method
    @classmethod
    def select_from_menu(cls, menu, print_msg):
        """Display a given selection menu and handle user selection.
        
        Temporarily switches to the provided menu screen, displays an optional
        message, processes user input, and returns to the previous screen.
        
        Args:
            menu (Screen): A menu Screen object (Shop, SelectRoom, Explore, etc.).
            print_msg (str | None): Optional message to display on the menu.
        
        Returns:
            int: Index of the selected item, -1 if cancelled, or menu-specific
                 special values (e.g., 3 for reroll in room selection).
        """
        mainscreen = cls.screen
        menu =  menu
        cls.screen = menu    #set as current screen
        if print_msg is not None :
            cls.screen.print(print_msg)
        selected = menu.select()
        cls.screen = mainscreen    #set as current screen
        cls.screen.update()
        return selected

    @classmethod
    def select_room(cls, rooms, print_msg=None):
        """Display a room selection menu for the player to choose a room.
        
        Args:
            rooms (list[Room]): List of Room objects available for selection.
            print_msg (str | None): Optional message to display above the menu. Defaults to None.
        
        Returns:
            int: Index of the selected room (0-2), -1 if cancelled, 3 if reroll requested.
        """
        return cls.select_from_menu(SelectRoom(rooms), print_msg)

    @classmethod
    def shop(cls, items, print_msg=None):
        """Display a shop menu for purchasing items.
        
        Args:
            items (list[tuple[str, int]]): List of (name, coin_cost) tuples for available items.
            print_msg (str | None): Optional message to display above the menu. Defaults to None.
        
        Returns:
            int: Index of the selected item (0-8 for individual selection) or -1 if cancelled.
        
        Note:
            Only the first 9 items are displayed and selectable in the shop interface.
        """
        return cls.select_from_menu(Shop(items), print_msg)
    
    @classmethod
    def explore(cls, items, color, print_msg=None):
        """Display an exploration menu for finding items in a room.
        
        Args:
            items (list[tuple[str, int, str]]): List of (name, count, category) tuples.
                         Category must be one of: 'consumable', 'permanent', 'other'.
            color (str): The color of the room being explored (cannot be yellow).
            print_msg (str | None): Optional message to display above the menu. Defaults to None.
        
        Returns:
            int: Index of the selected item (0-5), -1 if cancelled, or len(items[:6]) to take all.
        
        Note:
            Only the first 6 items are displayed and selectable in the explore interface.
        """
        return cls.select_from_menu(Explore(items, color), print_msg)

    @classmethod
    def game_over(cls):
        """Display the game over screen.
        
        Shows the game over screen and prompts the player to choose between
        starting a new game or quitting.
        
        Returns:
            int: 0 to start a new game, 1 to quit.
        """
        cls.screen = EndScreen('Game over !')
        return cls.screen.select()
        
    @classmethod
    def game_won(cls):
        """Display the won game screen.
        
        Shows the victory screen and prompts the player to choose between
        starting a new game or quitting.
        
        Returns:
            int: 0 to start a new game, 1 to quit.
        """
        cls.screen = EndScreen('You won !!!')
        return cls.screen.select()

    @staticmethod
    def quit_game():
        """Clean up pygame and exit the game.
        
        Properly quits the pygame module and raises SystemExit to terminate
        the application gracefully.
        
        Raises:
            SystemExit: Always raised to terminate the application.
        """
        pygame.quit()
        raise SystemExit()  # or sys.exit()

    @classmethod
    def event_listener(cls):
        """Process pygame events and dispatch them to the current screen's event handler.

        This method polls pygame events and maps them to the corresponding
        methods on the active screen's `event_handler` object. It handles
        application quit and window resize events directly via the `UI` and
        `Window` helpers, and forwards keyboard events to the following
        `event_handler` methods when present:

        - `escape()` : Escape key or cancel
        - `space()`  : Spacebar (often used to select multiple/all)
        - `enter()`  : Enter/Return specific selection
        - `back()`   : Backspace (unused in current menus)
        - `up()` / `down()` / `left()` / `right()` : Navigation keys (WASD/ZQSD or arrows)
        - `explore()` : 'i' key opens room exploration

        Returns:
            None
        """
        event_handler = cls.screen.event_handler
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                UI.quit_game()
            elif event_type == pygame.WINDOWRESIZED or event_type == pygame.WINDOWSIZECHANGED:
                cls.window.set_window_size(event.x,event.y)
                cls.screen.update()
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
                elif event_key == pygame.K_i:
                    event_handler.explore()




