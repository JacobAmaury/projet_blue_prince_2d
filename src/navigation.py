from player import Player
from ui_lib.event_handler import EventHandler
from player import Room
import random
import database
import player

class NavHandler(EventHandler):
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

    @staticmethod
    def enter():
        if Nav.shop_room is not None:
            x, y = Nav.shop_room
            Nav.open_shop(x, y)

        if Nav.dig_room is not None:
            x, y = Nav.dig_room
            Nav.dig(x, y)
            return
        
        if Nav.coffer_room is not None:
            x, y = Nav.coffer_room
            Nav.open_coffer(x, y)
            return
    
    @staticmethod
    def explore():
        Nav.open_current_room_explore()
    

        
class Nav :
    
    shop_room = None
    coffer_room = None
    dig_room = None 
    
    @classmethod
    def ini(cls,UI):            #initialise the class
        cls.ui = UI.ini()
        cls.ui.loadgame()
        cls.new_game()          #start a new game
        return cls

    @classmethod
    def new_game(cls):
        cls.player= Player(cls.ui)                      # creates inventory,map,...
        cls.ui.show_mainScreen(cls.player, NavHandler)  # creates and blits main_screen with data of player
        cls.inventory, cls.map = cls.player.inventory, cls.player.map

        cls.three_rooms = [[[[]for r in range(4)] for y in range(9)] for x in range(5)]  #x, y, rooms[0, 1, 2]
        cls.pool = cls.map.init_pool()
        cls.proba_pool = cls.map.update_proba_pool()

    @classmethod
    def game_won(self):
        Nav.ui.game_won()
        Nav.ui.quit_game()
        
    @classmethod
    def game_over(self):
        Nav.ui.game_over()
        Nav.new_game()

    @classmethod
    def pool_room(cls, proba_pool):
        return random.choice(proba_pool)

    @classmethod
    def all_cost_gems(cls, three_rooms):
        for room in three_rooms:
            if room.data['gem'] >= 0:
                return False
        return True
    
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
        if cls.three_rooms[next_x][next_y][r] == [] : 
            attempts = 0
            max_attempts = 1000
            while len(cls.three_rooms[next_x][next_y][r]) < 3  and attempts < max_attempts:
                new_room_name = cls.pool_room(cls.proba_pool)
                doors = database.rooms[new_room_name]['doors']
                room_doors_valid, rotation = cls.map.doors_layout(doors, next_x, next_y, r)

                if room_doors_valid and (new_room_name not in [room.name for room in cls.three_rooms[next_x][next_y][r]]):  
                    if cls.map.room_placement_condition(new_room_name, next_x, next_y):
                        cls.three_rooms[next_x][next_y][r].append(Room(new_room_name,rotation)) 
                                    
                if len(cls.three_rooms[next_x][next_y][r]) == 3 and cls.all_cost_gems(cls.three_rooms[next_x][next_y][r]):
                    cls.three_rooms[next_x][next_y][r] = []

                attempts += 1 
            if attempts >= max_attempts:
                raise RuntimeError(
                    f"Cannot find a valid room for ({next_x}, {next_y}). "
                    f"Only found {len(cls.three_rooms[next_x][next_y][r])} valid rooms."
                )
        return cls.three_rooms[next_x][next_y][r]
    
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

        #Block doors leading to a wall and level up the doors of the new room
        new_room.doors = cls.map.block_door(new_room.doors, next_x, next_y)
        new_room.doors = cls.map.level_up_door(new_room.doors, next_y)

        #create room with items and add doors to map 
        cls.map.add_room(new_room, next_position)
        cls.map.item_randmon_room(new_room.name, next_x, next_y)

        #Unlock the front door
        front = (r+2) % 4 #Change the rotation to the front of the room
        cls.map.rooms[next_x][next_y].doors[front] = -1 #set to opened
        
        # print(new_room_name)
        Effect().apply_effect(new_room.name)

        # remove room from the pool_room
        if new_room.name in cls.pool : 
            cls.pool.remove(new_room.name)
            cls.proba_pool = cls.map.update_proba_pool()

        #move the player and check if he lost
        cls.player.move(next_x, next_y, r)
        cls.check_room_actions(next_x, next_y)
        cls.open_explore_menu(next_x, next_y)
        cls.inventory.change_consumable('steps', -1)
        if cls.inventory.consumables['steps'] <= 0:
            cls.game_over()


    @classmethod
    def door_level_check(cls, door):
        cls.print_msg = None
        player_got_key = cls.inventory.consumables["key"] >= 1
        if door == 1 or door == -1:
            return True
        elif door == 2 and ('Lockpick_Kit' in cls.inventory.permanents):
            cls.print_msg = 'Lockpick kit used'
            return True
        elif door == 2 and player_got_key:
            cls.inventory.change_consumable('key', -1)
            cls.print_msg = '1 key used'
            return True
        elif door == 3 and player_got_key:
            cls.inventory.change_consumable('key', -1)
            cls.print_msg = '1 key used'
            return True
        if door != 0 : #not a wall
            cls.ui.screen.print("Can't open, not enough keys !")
        return False   

    @classmethod
    def enough_consumables(cls, new_room_name):
        """
        return False if the player doesn't have enough 'coin' or 'gem'
        """
        room_consumables = database.rooms[new_room_name]
        for consumable, increment in room_consumables.items():
            if consumable in ['coin', 'gem']:
                if increment < 0:
                    if (cls.inventory.consumables[consumable] + increment) < 0:
                        cls.ui.screen.print(f"Not enough {consumable}s !")
                        return False
        return True
    
    @classmethod
    def change_player_consumables(cls, new_room):
        """
        Apply the room's consumable effects to the player:
        - Subtract if the room costs items
        - Add if the room gives rewards
        """
        room_consumables = database.rooms[new_room.name]
        for consumable, increment in room_consumables.items():
            if consumable in database.consumables:
                cls.inventory.change_consumable(consumable, increment)

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

        door_can_be_opened = cls.door_level_check(cls.map.rooms[x][y].doors[r])
        if door_can_be_opened: 
            #unlock door # -> open_door
            cls.map.rooms[x][y].doors[r] = -1    #set to opened

            if next_x == 2 and next_y == 8:
                cls.game_won()

            cls.player.move(x,y,r)  #acctualise door_status on ui
            # print("Inventaire salle", cls.map.rooms_inventory[x][y])
            
            if cls.map.room_exists(next_x, next_y):
                next_room_has_a_door = cls.map.rooms[next_x][next_y].doors[(r+2)%4] != 0
                if next_room_has_a_door :
                    cls.map.rooms[next_x][next_y].doors[(r+2)%4] = -1 #set to opened
                    # r = (r+2) % 4 #Change the player rotation when entering a room
                    cls.inventory.change_consumable('steps', -1)
                    if cls.inventory.consumables['steps'] <= 0:
                        cls.game_over()
                    cls.player.move(next_x, next_y, r)
                    cls.check_room_actions(next_x, next_y)
                    cls.open_explore_menu(next_x, next_y)


            else:
                REROLL = 3; CANCEL = -1
                new_room_id = REROLL
                while(new_room_id == REROLL):
                    cls.three_room_choice(next_x, next_y, r)
                    new_room_id = cls.ui.select_room(cls.three_rooms[next_x][next_y][r], cls.print_msg)
                    if new_room_id == REROLL:
                        cls.inventory.change_consumable('dice', -1)
                        cls.three_rooms[next_x][next_y][r] = []
                        cls.print_msg = None

                if new_room_id != CANCEL:
                    new_room = cls.three_rooms[next_x][next_y][r][new_room_id]
                    if cls.enough_consumables(new_room.name):
                        cls.change_player_consumables(new_room)
                        cls.open_room(next_x, next_y, new_room)

    @classmethod
    def open_explore_menu(cls, x, y):

        room_inv = cls.map.rooms_inventory[x][y]

        #filter the objects
        items = []
        for name, count in room_inv.items():
            if count > 0:
                if name in database.consumables:
                    category = "consumable"
                elif name in database.permanents:
                    category = "permanent"
                else:
                    category = "other"
                items.append((name, count, category))

        if not items:
            return  

        # color for the room display
        color = cls.map.rooms[x][y].data["color"]
        if color == 'yellow':
            return

        selected = cls.ui.explore(items, color)

        if selected == -1:
            return

        if selected < len(items):
            name, nb, category = items[selected]
            cls.take_item(x, y, name, nb, category)

        else:
            for name, nb, category in items:
                cls.take_item(x, y, name, nb, category)

    @classmethod
    def open_current_room_explore(cls):
        x, y, _ = cls.player.position
        cls.open_explore_menu(x, y)



    @classmethod
    def take_item(cls, x, y, name, nb, category):
        inv = cls.player.inventory

        if category == "consumable":
            inv.change_consumable(name, nb)
        elif category == "permanent":
            for i in range(nb):
                inv.add_permanent(name)
        elif category == "other":
            if name == "apple":
                inv.change_consumable('steps', 2)


        cls.map.rooms_inventory[x][y][name] = 0


    @classmethod
    def check_room_actions(cls, x, y):
        room = cls.map.rooms[x][y]
        color = room.data["color"]

        # Reset possible actions
        cls.shop_room = None
        cls.dig_room = None
        room.message = None  # clear message

        message = ""

        if color == "yellow":
            message += "Press Enter to open the shop. "
            cls.shop_room = (x, y)

        if color == "green" and "Shovel" in cls.inventory.permanents and not room.dig:
            message += "Press Enter to dig. "
            cls.dig_room = (x, y)

        if cls.map.rooms_inventory[x][y]["coffer"] > 0 and not room.opened_coffer and color != "yellow":
            if cls.inventory.consumables["key"] > 0 or "Power_Hammer" in cls.inventory.permanents:
                message += "Press Enter to open the coffer. "
                cls.coffer_room = (x, y)
            else:
                message += "You need a key to open a coffer. "


        room.message = message

        # refresh screen
        cls.ui.screen.update_current_room()


    
    @classmethod
    def open_shop(cls, x, y):
        room = cls.map.rooms[x][y]

        items_for_sale = [
            ("key", 5),
            ("gem", 10),
            ("dice", 12),
            ("Shovel", 25)
        ]

        choice = cls.ui.shop(items_for_sale)

        if choice == -1:
            return

        # selected item
        name, price = items_for_sale[choice]

        # check coins
        if cls.inventory.consumables["coin"] < price:
            cls.ui.screen.print("Not enough coins !")
            return

        # buy
        cls.inventory.change_consumable("coin", -price)

        # add to inventory
        if name in database.consumables:
            cls.inventory.change_consumable(name, 1)
        elif name in database.permanents:
            cls.inventory.add_permanent(name)

        cls.ui.screen.print(f"You bought {name} !")


    @classmethod
    def dig(cls, x, y):
        room = cls.map.rooms[x][y]
        room.message = None
        room.dig = True 
        cls.dig_room = None

        loot_table = [
            ("coin", 2),
            ("coin", 5),
            ("gem", 1),
            ("key", 1),
            ("apple", 1),
            ("nothing", 0)
        ]

        loot, amount = random.choice(loot_table)

        if loot == "nothing":
            cls.ui.screen.print("You found nothing...")
            return

        if loot in cls.inventory.consumables:
            cls.inventory.change_consumable(loot, amount)
        else:
            if loot == "apple":
                cls.inventory.change_consumable("steps", 2) 

        cls.ui.screen.print(f"You found {amount} {loot} !")


    @classmethod
    def open_coffer(cls, x, y):
        room = cls.map.rooms[x][y]
        room.opened_coffer = True
        cls.coffer_room = None
        room.message = None

        if "Power_Hammer" not in cls.inventory.permanents:
            cls.inventory.change_consumable("key", -1)
            
        cls.map.rooms_inventory[x][y]["coffer"] = 0  

        loot_table = [
            ("gem", 2),
            ("coin", 3),
            ("key", 1),
            ("dice", 1),
            ("apple", 1),
            ("Shovel", 1),
            ("Lockpick_Kit", 1),
            ("Power_Hammer", 1),
            ('Lucky_Rabbits_Foot', 1)
        ]

        loot, amount = random.choice(loot_table)

        if loot in cls.inventory.consumables:
            cls.inventory.change_consumable(loot, amount)
        elif loot in database.permanents:
            for _ in range(amount):
                cls.inventory.add_permanent(loot)
        else:
            if loot == "apple":
                cls.inventory.change_consumable("steps", 2 * amount)

        room.message = ""
        cls.ui.screen.update_current_room()
        
        cls.ui.screen.print(f"You found {amount} {loot} inside the coffer !")
        









                        




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
        elif act_effect ==10:
            self.draft_new_rooms_10(room_name)
            
        

        
    
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
                    
        Nav.proba_pool = Nav.map.update_proba_pool()
        
        


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
                        
                        rand_index = random.randint(0,len(apple_pool)-1) 
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
                        
                        rand_index = random.randint(0,len(gem_pool)-1) 
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
                        rand_index = random.randint(0,len(item_pools)-1)
                        act_item = item_pools[rand_index]
                        if act_item != 0:
                            Nav.player.map.rooms_inventory[x][y][act_item] += 1

    def draft_new_rooms_10(self, room_name):
        database.rooms["PumpRoom"]['rarity'] += 3
        Nav.proba_pool = Nav.map.update_proba_pool()
        

