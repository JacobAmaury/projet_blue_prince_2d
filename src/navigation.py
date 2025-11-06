from player import Player
import random
import database
import player

class Nav :
    @classmethod
    def ini(cls,UI):            #initialise the class
        cls.ui = UI.ini()
        cls.new_game()          #start a new game
        return cls

    @classmethod
    def new_game(cls):
        cls.player = Player(cls.ui)      # creates inventory,map,...
        cls.ui.set_player(cls.player)   # ui displays data from this player
        cls.ui.mainScreen()             # creates and blits main_screen
        cls.inventory, cls.map = cls.player.inventory, cls.player.map

        cls.in_menu_selection = False
        cls.three_rooms = [[[] for y in range(9)] for x in range(5)]  #x, y, rooms[0, 1, 2]
        cls.three_rotations = [[{} for y in range(9)] for x in range(5)]  #x, y, rotation{0, 1, 2}
        cls.pool = cls.map.init_pool()
        cls.proba_pool = cls.map.update_proba_pool()
        cls.room_inventory = cls.map.rooms_inventory

        cls.ui.event_handler.space = cls.player_move
        cls.ui.event_handler.up = cls.up
        cls.ui.event_handler.down = cls.down
        cls.ui.event_handler.left = cls.left
        cls.ui.event_handler.right = cls.right

    @classmethod
    def up(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 2)

    @classmethod
    def down(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 0)

    @classmethod
    def left(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 3)
        else:
            if cls.ui.room_choice > 0:
                cls.ui.room_choice -= 1 

    @classmethod
    def right(cls):
        if not(cls.in_menu_selection):
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 1)
        else:
            if cls.ui.room_choice < 3:
                cls.ui.room_choice += 1 
    
    @classmethod
    def pool_room(cls, proba_pool):
        return random.choice(proba_pool)
    
    @classmethod
    def room_exist(cls, next_x, next_y):
        rooms = cls.map.rooms
        room_exist = False
        for _, coords_list in rooms.items():
            for c in coords_list:
                if (c[0], c[1]) == (next_y, next_x):
                    room_exist = True
                    break
        return room_exist


    @classmethod
    def three_room_choice(cls, next_x, next_y, r):
        """
        Chooses up to three valid rooms for the given map position.

        Checks door alignment and rotation compatibility, stores valid rooms 
        and their rotations at (next_x, next_y).

        Args:
            next_x (int): X-coordinate on the map.
            next_y (int): Y-coordinate on the map.
            r (int): Rotation index.

        Returns:
            dict: Rooms mapped to their valid rotations.
        """
        index_next_x = next_x + 2
        if cls.three_rooms[index_next_x][next_y] == [] : 
            while len(cls.three_rooms[index_next_x][next_y]) < 3:
                new_room = cls.pool_room(cls.proba_pool)
                doors = database.rooms[new_room]["doors"]
                room_doors_valid, rotation = cls.map.doors_layout(doors, next_x, next_y, r)

                if room_doors_valid and (new_room not in cls.three_rooms[index_next_x][next_y]):
                    cls.three_rooms[index_next_x][next_y].append(new_room) 
                    cls.three_rotations[index_next_x][next_y][new_room] = rotation
        return cls.three_rotations[index_next_x][next_y]
    
    @classmethod
    def open_room(cls, next_x, next_y, rotations, new_room_name):
        """
        Opens and places a new room at the given coordinates.

        Updates the map, room inventory, and player state, removing the room 
        from the pool and adjusting probabilities.
        """
        y, x, r = cls.map.player_position
        index_next_x = next_x + 2

        cls.three_rooms[index_next_x][next_y] = []
        next_position = (next_y, next_x, rotations[new_room_name])

        cls.room_inventory[next_x][next_y] = database.rooms[new_room_name]

        doors = database.rooms[new_room_name]["doors"]
        for i in range(rotations[new_room_name]):
            doors = cls.map.rot_doors(doors)

        cls.map.add_room(new_room_name, next_position, doors)

        if new_room_name in cls.pool : 
            cls.pool.remove(new_room_name)
            cls.proba_pool = cls.map.update_proba_pool()

        cls.player.move_player_position(next_y, next_x, r)
        cls.inventory.change_consumable('steps', -1)
        if cls.inventory.consumables['steps'] <= 0:
            cls.player.game_over()
        

    @classmethod
    def door_level_check(cls, door): #for future usage
        doors_open = False
        if door == 1:
            doors_open == True
        elif door == 2:
            if ('Lockpick_Kit' in cls.inventory.permanents) or (cls.inventory.consumables["key"]>= 1):
                cls.inventory.change_consumable('key', -1)
                doors_open == True
        elif door == 3:
            if (cls.inventory.consumables["key"]>= 1):
                cls.inventory.change_consumable('key', -1)
                doors_open == True
        return doors_open        


    @classmethod
    def player_move(cls):
        """
        Handles player movement and room entry logic.

        Moves the player forward if possible or triggers room selection when 
        entering an unexplored area.
        """
        if not(cls.in_menu_selection):
            #(0,0,0) : (bottom,center,0°), rot:(0:0°,1:90°,2:180°,3:-90°)
            y, x, r = cls.map.player_position
            next_y, next_x = y, x

            if r == 0 : #bottom
                next_y = y - 1 
            elif r == 1: #right
                next_x = x + 1
            elif r == 2 : #top
                next_y = y + 1 
            elif r == 3: #left
                next_x = x - 1

            doors_open = cls.map.doors_map[x+2][y][r] == 1
            if doors_open: 

                if next_x == 0 and next_y == 8:
                    cls.player.game_won()

                if cls.room_exist(next_x, next_y):
                    # r = (r+2) % 4 #Change the player rotation when entering a room
                    cls.inventory.change_consumable('steps', -1)
                    if cls.inventory.consumables['steps'] <= 0:
                        cls.player.game_over()
                    cls.player.move_player_position(next_y, next_x, r)
                else:
                    index_next_x = next_x + 2

                    new_room_name = "Reroll"
                    while(new_room_name == "Reroll"):

                        rotations = cls.three_room_choice(next_x, next_y, r)

                        cls.in_menu_selection = True
                        new_room_name = cls.ui.selection_menu(cls.three_rooms[index_next_x][next_y], rotations)
                        cls.in_menu_selection = False

                        if new_room_name not in (None, "Reroll"):
                            cls.open_room(next_x, next_y, rotations, new_room_name)

                        if new_room_name == "Reroll":
                            cls.three_rooms[index_next_x][next_y] = []
                            cls.three_rotations[index_next_x][next_y] = {}

                        

                        




class Effect:

    def apply_effect(room_name):
        
        return None
    
    def room_rarity_5(room_name):
        #modify the rarity of room_name to an lower value

        if room_name == "Solarium":
            for i in range(len(database.rooms)):
                if database.rooms[i]["rarity"] == 2 or database.rooms[i]["rarity"] == 3 or database.rooms[i]["rarity"] == 1:
                    database.rooms[i]["rarity"] -= 1
                    
        if room_name == "Furnace": 
            for i in range(len(database.rooms)):
                if database.rooms[i]["color"] == "red" and database.rooms[i]["rarity"] > 1:
                    database.rooms[i]["rarity"] -= 1

        if room_name == "Greenhouse":
            for i in range(len(database.rooms)):
                if database.rooms[i]["colot"] == "green" and database.rooms[i]["rarity"] > 1:
                    database.rooms[i]["rarity"] -= 1

    def set_gem_number_8(room_name):
        if room_name == "Ballroom":
            player.Inventory.consumables['gem'] = 2

    def divide_steps_by_2_9(room_name):
        if room_name == "Library" or "WeightRoom":
            player.Inventory.consumables['steps'] //= 2

        