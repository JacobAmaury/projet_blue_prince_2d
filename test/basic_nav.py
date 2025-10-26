import __src_path   #set path ../src


from player import Player                 # pyright: ignore[reportMissingImports]

class Nav :
    @classmethod
    def ini(cls,UI):            #initialise the class
        cls.ui = UI.ini()
        cls.new_game()          #start a new game
        return cls

    @classmethod
    def new_game(cls):
        player= Player(cls.ui)      # creates inventory,map,...
        cls.ui.set_player(player)   # ui displays data from this player
        cls.ui.mainScreen()             # creates and blits main_screen
        cls.inventory, cls.map = player.inventory, player.map