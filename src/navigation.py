from player import Player
import random
import database

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
        cls.three_rooms = [[[] for y in range(9)] for x in range(5)]  #x, y, rooms[0, 1, 2]
        cls.three_rotations = [[{} for y in range(9)] for x in range(5)]  #x, y, rotation{0, 1, 2}
        cls.pool = cls.map.init_pool()
        cls.proba_pool = cls.map.update_proba_pool()

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
    
    @classmethod
    def pool_room(cls, proba_pool):
        return random.choice(proba_pool)

    @classmethod
    def three_room_choice(cls, next_x, next_y, r):
        index_next_x = next_x + 2
        if cls.three_rooms[index_next_x][next_y] == [] : 
            while len(cls.three_rooms[index_next_x][next_y]) < 3:
                new_room = cls.pool_room(cls.proba_pool)
                doors = database.rooms[new_room]["doors"]
                room_doors_valid, rotation = cls.map.doors_layout(doors, next_x, next_y, r)

                if room_doors_valid:
                    cls.three_rooms[index_next_x][next_y].append(new_room) 
                    cls.three_rotations[index_next_x][next_y][new_room] = rotation
        return cls.three_rotations[index_next_x][next_y]
    
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

            if r == 0 : #bottom
                next_y = y - 1 
            elif r == 1: #right
                next_x = x + 1
            elif r == 2 : #top
                next_y = y + 1 
            elif r == 3: #left
                next_x = x - 1
            next_move_in_map = (-2 <= next_x <= 2) and (0 <= next_y <= 8)
            if next_move_in_map:
                room_exist = False
                for _, coords_list in rooms.items():
                    for c in coords_list:
                        if (c[0], c[1]) == (next_y, next_x):
                            room_exist = True
                            break
                if room_exist :
                    # r = (r+2) % 4 #Change the player rotation when entering a room
                    cls.map.move_player_position(next_y, next_x, r)
                else:
                    # to do : check if there is a door and its level
                    index_next_x = next_x + 2
                    rotations = cls.three_room_choice(next_x, next_y, r)

                    cls.in_menu_selection = True
                    new_room_name = cls.ui.selection_menu(cls.three_rooms[index_next_x][next_y], rotations)
                    cls.in_menu_selection = False



                    if new_room_name != None:
                        cls.three_rooms[index_next_x][next_y] = []
                        next_position = (next_y, next_x, rotations[new_room_name])

                        doors = database.rooms[new_room_name]["doors"]
                        for i in range(rotations[new_room_name]):
                            doors = cls.map.rot_doors(doors)

                        cls.map.add_room(new_room_name, next_position, doors)

                        if new_room_name in cls.pool : 
                            cls.pool.remove(new_room_name)
                            cls.proba_pool = cls.map.update_proba_pool()
                            print(len(cls.pool), len(cls.proba_pool))

                        cls.map.move_player_position(next_y, next_x, r)
      
                    if new_room_name == "Reroll":
                        cls.three_rooms[index_next_x][next_y] = []
                        rotations = cls.three_room_choice(next_x, next_y, r)



