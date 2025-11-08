from player import Player
from ui_lib.event_handler import EventHandler
from player import Room
import random
import database
import player
import random as rd

class NavHandlers(EventHandler):
    @staticmethod
    def space():
        Nav.player_move()
    @staticmethod
    def up():
        x, y, _ = Nav.player.position
        Nav.player.move(x, y, 2)
    @staticmethod
    def down():
        x, y, _ = Nav.player.position
        Nav.player.move(x, y, 0)
    @staticmethod
    def left():
        x, y, _ = Nav.player.position
        Nav.player.move(x, y, 3)
    @staticmethod
    def right():
        x, y, _ = Nav.player.position
        Nav.player.move(x, y, 1)
        
class Nav :
    @classmethod
    def ini(cls,UI):            #initialise the class
        cls.ui = UI.ini()
        cls.new_game()          #start a new game
        return cls

    @classmethod
    def new_game(cls):
        cls.player= Player(cls.ui)                  # creates inventory,map,...
        cls.ui.mainScreen(cls.player)               # creates and blits main_screen with data of player
        cls.inventory, cls.map = cls.player.inventory, cls.player.map
        cls.ui.screen.event_handler = NavHandlers

        cls.three_rooms = [[[] for y in range(9)] for x in range(5)]  #x, y, rooms[0, 1, 2]
        cls.pool = cls.map.init_pool()
        cls.proba_pool = cls.map.update_proba_pool()

    @classmethod
    def pool_room(cls, proba_pool):
        return random.choice(proba_pool)

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
        if cls.three_rooms[next_x][next_y] == [] : 
            attempts = 0
            max_attempts = 1000
            while len(cls.three_rooms[next_x][next_y]) < 3  and attempts < max_attempts:
                new_room_name = cls.pool_room(cls.proba_pool)
                doors = database.rooms[new_room_name]['doors']
                room_doors_valid, rotation = cls.map.doors_layout(doors, next_x, next_y, r)

                if room_doors_valid and (new_room_name not in [room.name for room in cls.three_rooms[next_x][next_y]]):  
                    cls.three_rooms[next_x][next_y].append(Room(new_room_name,rotation)) 
                attempts += 1 
            if attempts >= max_attempts:
                raise RuntimeError(
                    f"Cannot find a valid room for ({next_x}, {next_y}). "
                    f"Only found {len(cls.three_rooms[next_x][next_y])} valid rooms."
                )
        return cls.three_rooms[next_x][next_y]
    
    @classmethod
    def open_room(cls, next_x, next_y, new_room):
        """
        Opens and places a new room at the given coordinates.

        Updates the map, room inventory, and player state, removing the room 
        from the pool and adjusting probabilities.
        """
        _, _, r = cls.player.position

        cls.three_rooms[next_x][next_y] = []
        next_position = (next_x, next_y)

        #rotate and level up the doors of the new room
        new_room.doors = cls.map.rot_doors(new_room.doors, new_room.rotation)
        new_room.doors = cls.map.level_up_door(new_room.doors, next_y)

        #create room with items and add doors to map 
        cls.map.add_room(new_room, next_position)
        cls.map.item_randmon_room(new_room.name, next_x, next_y)

        #Unlock the front door
        front = (r+2) % 4 #Change the rotation to the front of the room
        cls.map.rooms[next_x][next_y].doors[front] = 1
        
        # print(new_room_name)
        Effect().apply_effect(new_room.name)

        # remove room from the pool_room
        if new_room.name in cls.pool : 
            cls.pool.remove(new_room.name)
            cls.proba_pool = cls.map.update_proba_pool()

        #move the player and check if he lost
        cls.player.move(next_x, next_y, r)
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
    def change_player_consumables(cls, new_room, next_x, next_y):
        """
        Apply the room's consumable effects to the player:
        - Subtract if the room costs items
        - Add if the room gives rewards
        """
        room_consumables = database.rooms[new_room.name]
        for consumable, increment in room_consumables.items():
            if consumable in database.consumables:
                cls.inventory.change_consumable(consumable, increment)
                # Update room inventory for positive gains (except 'steps')
                if increment > 0 and consumable != 'steps':
                    cls.map.rooms_inventory[next_x][next_y][consumable] += increment
    @classmethod
    def player_move(cls):
        """
        Handles player movement and room entry logic.

        Moves the player forward if possible or triggers room selection when 
        entering an unexplored area.
        """
        #(0,0,0) : (left,bottom,0°), rot:(0:0°,1:90°,2:180°,3:-90°)
        x, y, r = cls.player.position
        next_y, next_x = y, x

        if r == 0 : #bottom
            next_y = y - 1 
        elif r == 1: #right
            next_x = x + 1
        elif r == 2 : #top
            next_y = y + 1 
        elif r == 3: #left
            next_x = x - 1

        doors_open = cls.door_level_check(cls.map.rooms[x][y].doors[r])
        if doors_open: 
            #unlock door
            cls.map.rooms[x][y].doors[r] = 1

            if next_x == 2 and next_y == 8:
                cls.player.game_won()

            # print("Inventaire salle", cls.map.rooms_inventory[x][y])
            
            no_wall = (0 <= next_x < 5) and (0 <= next_y < 9)
            if no_wall:
                if cls.map.room_exists(next_x, next_y):
                    # r = (r+2) % 4 #Change the player rotation when entering a room
                    cls.inventory.change_consumable('steps', -1)
                    if cls.inventory.consumables['steps'] <= 0:
                        cls.player.game_over()
                    cls.player.move(next_x, next_y, r)
                else:
                    reroll = 3; cancel = -1
                    new_room_id = 3 #reroll value
                    while(new_room_id == reroll):
                        cls.three_rooms[next_x][next_y] = cls.three_room_choice(next_x, next_y, r)
                        new_room_id = cls.ui.screen.room_select_menu(cls.three_rooms[next_x][next_y])

                        if new_room_id != reroll and  new_room_id != cancel:
                            new_room = cls.three_rooms[next_x][next_y][new_room_id]
                            if cls.enough_consumables(new_room.name):
                                cls.change_player_consumables(new_room, next_x, next_y)
                                cls.open_room(next_x, next_y, new_room)

                        if new_room_id == reroll:
                            cls.three_rooms[next_x][next_y] = []

                        

                        




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
    

    def spread_green_room_1_and_4(self, room_name):
        """take the room name if the room name is patio spread gems in all green room"""
        room_exists = Nav.map.room_exists

        if room_name == 'SecretGarden':
            apple_pool = [0]*50
            apple_pool.extend(['gem']*20)

            for y in range(9):
                for x in range(5):
                    if not room_exists(x,y):
                        continue
                    if database.rooms[Nav.map.rooms[x][y].name]['color'] == 'green': #verify if the room[x,y] is green
                        
                        rand_index = rd.randint(0,len(apple_pool)-1) 
                        act_item = apple_pool[rand_index] 

                        if act_item != 0: 
                            Nav.player.map.rooms_inventory[x][y]['apple'] += 1
            
        
        if room_name == 'Patio':
            gem_pool = [0]*50
            gem_pool.extend(['gem']*20)
            for y in range(9):
                for x in range(5):
                    if not room_exists(x,y):
                        continue
                    if database.rooms[Nav.map.rooms[x][y].name]['color'] == 'green': #verify if the room[x,y] is green
                        
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
        

