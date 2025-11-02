from player import Player

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
        cls.ui.event_handler.space = cls.player_move

    @classmethod
    def open_room(cls, room_name, position):
        cls.map.add_room(room_name, position)
        y, x, r = position
        cls.map.move_door(y, x, r)
    
    @classmethod
    def player_move(cls):
        """
        Control the player allowed movement
        """
        #(0,0,0) : (bottom,center,0°), rot:(0:0°,1:90°,2:180°,3:-90°)
        y, x, r = cls.map.door
        rooms = cls.map.rooms
        next_y, next_x = y, x

        if r == 0 : # bottom
            next_y = y - 1 
        elif r == 1: # to do : check if it left or right
            next_x = x + 1
        elif r == 2 : #top
            next_y = y + 1 
        elif r == 3: # to do :check if it left or right
            next_x = x - 1
        next_position = (next_y, next_x, r)
        next_move_in_map = (-2 < next_x < 2) and (0 < next_y < 9)
        if next_move_in_map:
            room_exist = False
            for _, coords_list in rooms.items():
                for c in coords_list:
                    if (c[0], c[1]) == (next_y, next_x):
                        room_exist = True
                        break

            if room_exist :
                cls.map.move_door(next_y, next_x, r)
            else:
                # to do : check if there is a door and its level
                new_room_name = cls.ui.selection_menu(rooms) 
                # cls.open_room(new_room_name, next_position)

            

