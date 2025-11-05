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
        cls.in_menu_selection = False
        cls.ui.event_handler.space = cls.player_move
        cls.ui.event_handler.up = cls.up
        cls.ui.event_handler.down = cls.down
        cls.ui.event_handler.left = cls.left
        cls.ui.event_handler.right = cls.right

    @classmethod
    def up(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.map.move_player_position(y, x , 2)

    @classmethod
    def down(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.map.move_player_position(y, x , 0)

    @classmethod
    def left(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.map.move_player_position(y, x , 3)
        else:
            if cls.ui.room_choice > 0:
                cls.ui.room_choice -= 1 

    @classmethod
    def right(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.map.move_player_position(y, x , 1)
        else:
            if cls.ui.room_choice < 3:
                cls.ui.room_choice += 1 
                print(cls.ui.room_choice)



    @classmethod
    def open_room(cls, room_name, position):
        cls.map.add_room(room_name, position)
        y, x, r = position
        cls.map.move_player_position(y, x, r)
    
    @classmethod
    def player_move(cls):
        """
        Control the player allowed movement
        """
        if not(cls.in_menu_selection):
            #(0,0,0) : (bottom,center,0°), rot:(0:0°,1:90°,2:180°,3:-90°)
            y, x, r = cls.map.player_position
            rooms = cls.map.rooms
            next_y, next_x = y, x

            if r == 0 : # bottom
                next_y = y - 1 
            elif r == 1: # right
                next_x = x + 1
            elif r == 2 : #top
                next_y = y + 1 
            elif r == 3: # left
                next_x = x - 1
            next_position = (next_y, next_x, r)
            next_move_in_map = (-2 <= next_x <= 2) and (0 <= next_y <= 8)
            if next_move_in_map:
                room_exist = False
                for _, coords_list in rooms.items():
                    for c in coords_list:
                        if (c[0], c[1]) == (next_y, next_x):
                            room_exist = True
                            break
                if room_exist :
                    r = (r+2) % 4 #Change the player rotation when entering a new room
                    cls.map.move_player_position(next_y, next_x, r)
                else:
                    # to do : check if there is a door and its level

                    three_rooms = []
                    #if three_rooms == [] : 
                        #while len(three_rooms) <= 3:
                            #choose new_room
                            #doors = new_room["doors"]
                            #room_doors_valid, rotation = cls.map.doors_layout(doors, next_x, next_y, r)
                            #if room_doors_valid:
                                #three_rooms += new_room

                    cls.in_menu_selection = True
                    new_room_name = cls.ui.selection_menu(rooms)
                    cls.in_menu_selection = False

                    if new_room_name != None:
                        cls.open_room(new_room_name, next_position)

            

