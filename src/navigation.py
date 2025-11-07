from player import Player
import random
import database
import player
import random as rd

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

        cls.menu = "map"
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
        if cls.menu == "map":
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 2)
        elif cls.menu == "item selection": 
            pass

    @classmethod
    def down(cls):
        if cls.menu == "map":
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 0)
        elif cls.menu == "item selection": 
            pass

    @classmethod
    def left(cls):
        if cls.menu == "map":
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 3)
        elif cls.menu == "room selection":
            if cls.ui.room_choice > 0:
                cls.ui.room_choice -= 1 
        elif cls.menu == "item selection": 
            pass

    @classmethod
    def right(cls):
        if cls.menu == "map":
            y, x, r = cls.map.player_position
            cls.player.move_player_position(y, x , 1)
        elif cls.menu == "room selection":
            if cls.ui.room_choice < 3:
                cls.ui.room_choice += 1 
        elif cls.menu == "item selection": 
            pass
    
    @classmethod
    def pool_room(cls, proba_pool):
        return random.choice(proba_pool)
    
    @classmethod
    def room_exist(cls, next_x, next_y):
        rooms = cls.map.rooms
        room_exist = False
        for coords_list in rooms.values():
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
            attempts = 0
            max_attempts = 1000
            while len(cls.three_rooms[index_next_x][next_y]) < 3  and attempts < max_attempts:
                new_room = cls.pool_room(cls.proba_pool)
                doors = database.rooms[new_room]["doors"]
                room_doors_valid, rotation = cls.map.doors_layout(doors, next_x, next_y, r)

                if room_doors_valid and (new_room not in cls.three_rooms[index_next_x][next_y]):
                    cls.three_rooms[index_next_x][next_y].append(new_room) 
                    cls.three_rotations[index_next_x][next_y][new_room] = rotation
                attempts += 1 
            if attempts >= max_attempts:
                raise RuntimeError(
                    f"Cannot find a valid room for ({next_x}, {next_y}). "
                    f"Only found {len(cls.three_rooms[index_next_x][next_y])} valid rooms."
                )
        return cls.three_rotations[index_next_x][next_y]
    
    @classmethod
    def open_room(cls, next_x, next_y, rotations, new_room_name):
        """
        Opens and places a new room at the given coordinates.

        Updates the map, room inventory, and player state, removing the room 
        from the pool and adjusting probabilities.
        """
        _, _, r = cls.map.player_position
        index_next_x = next_x + 2

        cls.three_rooms[index_next_x][next_y] = []
        next_position = (next_y, next_x, rotations[new_room_name])

        #rotate and level up the doors of the new room
        doors = database.rooms[new_room_name]["doors"]
        doors = cls.map.rot_doors(doors, rotations[new_room_name])
        doors = cls.map.level_up_door(doors, next_y)


        #create room with items and add doors to map 
        cls.map.add_room(new_room_name, next_position, doors)
        cls.map.item_randmon_room(new_room_name, next_x, next_y)

        #Unlock the front door
        front = (r+2) % 4 #Change the rotation to the front of the room
        cls.map.doors_map[index_next_x][next_y][front] = 1
        
        # print(new_room_name)
        Effect().apply_effect(new_room_name)

        # remove room from the pool_room
        if new_room_name in cls.pool : 
            cls.pool.remove(new_room_name)
            cls.proba_pool = cls.map.update_proba_pool()

        #move the player and check if he lost
        cls.player.move_player_position(next_y, next_x, r)
        cls.inventory.change_consumable('steps', -1)
        if cls.inventory.consumables['steps'] <= 0:
            cls.player.game_over()

        # #open item_selection_menu
        # cls.menu = "item selection"
        # new_room_name = cls.ui.item_selection_menu()
        # cls.menu = "map"  

    @classmethod
    def door_level_check(cls, door):
        player_got_key = cls.inventory.consumables["key"] >= 1
        if door == 0:
            doors_open = False
        if door == 1:
            doors_open = True
        elif door == 2 and ('Lockpick_Kit' in cls.inventory.permanents):
            doors_open = True
        elif door == 2 and player_got_key:
            cls.inventory.change_consumable('key', -1)
            doors_open = True
        elif door == 3 and player_got_key:
            cls.inventory.change_consumable('key', -1)
            doors_open = True
        return doors_open   

    @classmethod
    def enough_consumables(cls, new_room_name):
        """
        return False if the player doesn't have enough 'steps', 'coin' or 'gem'
        """
        room_consumables = database.rooms[new_room_name]
        for consumable, increment in room_consumables.items():
            if consumable in database.consumables:
                if increment < 0:
                    if (cls.inventory.consumables[consumable] + increment) < 0:
                        return False
        return True
    
    @classmethod
    def change_player_consumables(cls, new_room_name, index_next_x, next_y):
        """
        Apply the room's consumable effects to the player:
        - Subtract if the room costs items
        - Add if the room gives rewards
        """
        room_consumables = database.rooms[new_room_name]
        for consumable, increment in room_consumables.items():
            if consumable in database.consumables:
                cls.inventory.change_consumable(consumable, increment)

                # Update room inventory for positive gains (except 'steps')
                if increment > 0 and consumable != 'steps':
                    cls.map.rooms_inventory[index_next_x][next_y][consumable] += increment

    @classmethod
    def player_move(cls):
        """
        Handles player movement and room entry logic.

        Moves the player forward if possible or triggers room selection when 
        entering an unexplored area.
        """
        if cls.menu == "map":
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

            doors_open = cls.door_level_check(cls.map.doors_map[x+2][y][r])
            if doors_open: 
                #unlock door
                cls.map.doors_map[x+2][y][r] = 1

                if next_x == 0 and next_y == 8:
                    cls.player.game_won()

                # print("Inventaire salle", cls.map.rooms_inventory[x][y])
                
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

                        cls.menu = "room selection"
                        new_room_name = cls.ui.room_select_menu(cls.three_rooms[index_next_x][next_y], rotations)
                        cls.menu = "map"

                        if new_room_name not in (None, "Reroll"):
                            if cls.enough_consumables(new_room_name):
                                cls.change_player_consumables(new_room_name, index_next_x, next_y)
                                cls.open_room(next_x, next_y, rotations, new_room_name)

                        if new_room_name == "Reroll":
                            cls.three_rooms[index_next_x][next_y] = []
                            cls.three_rotations[index_next_x][next_y] = {}

                        

                        




class Effect:

    def apply_effect(self, room_name):
        act_effect = database.rooms[room_name]['effect']

        if act_effect in (1, 4):
            self.spread_green_room_1_and_4(room_name)
        elif act_effect == 2:
            self.spread_items_2_and_3('key', room_name)
        elif act_effect == 3:
            self.spread_items_2_and_3('coin', room_name)
        elif act_effect == 4:
            self.spread_green_room_1_and_4(room_name)
        elif act_effect == 5:
            self.room_rarity_5(room_name)
        elif act_effect == 6:
            self.modify_proba_item_6(room_name)
        elif act_effect == 7:
            pass
        elif act_effect == 8:
            self.set_gem_number_8(room_name)
        elif act_effect == 9:
            self.divide_steps_by_2_9(room_name)
            
        

        
    
    def room_rarity_5(self,room_name):
        #modify the rarity of room_name to an lower value

        if room_name == 'Solarium':
            for i in database.rooms:
                if database.rooms[i]['rarity'] == 2 or database.rooms[i]['rarity'] == 3 or database.rooms[i]['rarity'] == 1:
                    database.rooms[i]['rarity'] -= 1
                    
        if room_name == 'Furnace': 
            for i in database.rooms:
                if database.rooms[i]['color'] == "red" and database.rooms[i]['rarity'] > 0:
                    database.rooms[i]['rarity'] -= 1

        if room_name == 'Greenhouse':
            for i in database.rooms:
                if database.rooms[i]['color'] == 'green' and database.rooms[i]['rarity'] > 0:
                    database.rooms[i]['rarity'] -= 1
        


    def set_gem_number_8(self, room_name):
        if room_name == 'Ballroom':
            Nav.player.inventory.consumables['gem'] = 2


    def divide_steps_by_2_9(self, room_name):
        if room_name == 'Library' or 'WeightRoom':
            Nav.player.inventory.consumables['steps'] //= 2


    def modify_proba_item_6(self, room_name):
        player.Map.effect_6 = True


    @classmethod
    def room_ex(cls, next_x, next_y):
        rooms = Nav.player.map.rooms
        for name, coords_list in rooms.items():
            for c in coords_list:
                if (c[0], c[1]) == (next_y, next_x):
                    return name
        return None
    

    def spread_green_room_1_and_4(self, room_name):
        """take the room name if the room name is patio spread gems in all green room"""

        if room_name == 'SecretGarden':
            apple_pool = [0]*50
            apple_pool.extend(['gem']*20)

            for y in range(9):
                for x in range(5):
                    if self.room_ex(x,y) == None:
                        continue
                    if database.rooms[self.room_ex(x,y)]['color'] == 'green': #verify if the room[x,y] is green
                        
                        rand_index = rd.randint(0,len(apple_pool)-1) 
                        act_item = apple_pool[rand_index] 

                        if act_item != 0: 
                            Nav.player.map.rooms_inventory[x][y]['apple'] += 1
            
        
        if room_name == 'Patio':
            gem_pool = [0]*50
            gem_pool.extend(['gem']*20)
            for y in range(9):
                for x in range(5):
                    if self.room_ex(x,y) == None:
                        continue
                    if database.rooms[self.room_ex(x,y)]['color'] == 'green': #verify if the room[x,y] is green
                        
                        rand_index = rd.randint(0,len(gem_pool)-1) 
                        act_item = gem_pool[rand_index] 

                        if act_item != 0: 
                            Nav.player.map.rooms_inventory[x][y]['gem'] += 1


    def spread_items_2_and_3(self, item_to_spread, room_name):

        item_pools = [0]*50
        rarity_weights = {
            'coin': 20,
            'gem': 20,
            'key': 20,
            'dice': 10,
        }
        
        item_pools.extend([item_to_spread]*rarity_weights[item_to_spread]) 

        for y in range(9):
            for x in range(5):
                if Nav.player.map.rooms_inventory[x][y]:
                    for i in range(4):
                        rand_index = rd.randint(0,len(item_pools)-1)
                        act_item = item_pools[rand_index]
                        if act_item != 0:
                            Nav.player.map.rooms_inventory[x][y][act_item] += 1
        




                

        