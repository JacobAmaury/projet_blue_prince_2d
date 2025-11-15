import database
import random as rd

class Player :
    def __init__(self,ui):
        Player.ui = ui
        self.map = Map()
        self.inventory = Inventory()
        self.position = (2,0,0)
        x,y,r = self.position
        self.current_room = self.map.rooms[x][y]
        self.door_status = self.map.rooms[x][y].doors[r]

    def move(self,x,y,r): #move_player_position
        """(0,0,0) : (bottom,left,0°)  rot:(0:0°,1:90°,2:180°,3:-90°)"""
        #position : (x,y,r) with x in [0,4], y in [0,8], r in [0,3]
        self.position = x,y,r
        # door_status =  -1:opened, 0:wall, 1:closed, 2:1_lock, 3:2_lock
        self.current_room = self.map.rooms[x][y]
        self.door_status = self.map.rooms[x][y].doors[r]
        Player.ui.screen.update_player_position()


class Inventory:
    def __init__(self):
        self.consumables = {'steps': 70, 'coin': 0, 'gem': 2, 'key': 0, 'dice': 0}
        self.permanents = []    #sets display order

    def change_consumable(self,name,increment):
        self.consumables[name] += increment
        Player.ui.screen.update_consumables()

    def add_permanent(self,name):
        if name not in database.permanents :
            raise ValueError('name not in database')
        if name not in self.permanents:
            self.permanents.append(name)
        Player.ui.screen.update_permanents()

class Room :
    def __init__(self, name, rotation=0):
        self.name = name
        self.rotation = rotation
        self.data = database.rooms[name]
        self.doors = Map.rot_doors(self.data['doors'][:], rotation)  #copy by value if room has multiple instances
        self.message = None # displayed msg : invite player to press Enter for shop, explore,...
        #self.inventory ?
        self.dig = False
        self.opened_coffer = False
    
    def __str__(self):
        return (
            f"Room('{self.name}', rotation={self.rotation})\n"
            f"  Doors: {self.doors}\n"
            f"  Data: {self.data}"
        )

class Map :
    def __init__(self):
        self.rooms = [[None for y in range(9)] for x in range(5)]  #x, y
        self.rooms[2][0] = Room('EntranceHall')
        self.rooms_inventory =  [[{
            "coin": 0,
            "gem": 0,
            "key": 0,
            "dice": 0,
            "apple":0,
            "Shovel": 0,
            "Power_Hammer": 0,
            'Lucky_Rabbits_Foot': 0,
            "Lockpick_Kit": 0,
            "Metal_Detector":0,
            "coffer" : 0
        } for y in range(9)] for x in range(5)]  #x, y, database_element

    def add_room(self,room,position):
        x, y = position
        #position : (x,y), x in [0,4], y in [0,8]
        self.rooms[x][y] = room
        Player.ui.screen.update_map()

    def room_exists(self, next_x, next_y):
        return self.rooms[next_x][next_y] is not None


    def room_placement_condition(self, name, x, y):
        """
        Returns True if the given room can be placed at (x, y)
        according to known Blue Prince floorplan restrictions.

        Args:
            name (str): room name
            x (int): column (0–4)
            y (int): row (0–8)

        Returns:
            bool: True if placement is allowed, False otherwise
        """
        max_x=4; max_y=8
        edge_y = (y == 0 or y == max_y)
        edge_x = (x == 0 or x == max_x)
        corner = (x in [0, max_x] and y in [0, max_y])
        
        conditions = {
            "Veranda": edge_y or edge_x,
            "Patio": edge_x,
            "Solarium": edge_y,
            "WestWingHall": x == 0,
            "EastWingHall": x == max_x
        }

        if name in conditions:
            return conditions[name]
        return True  # default: no restriction

    def init_pool(self):
        #add one time every rooms
        self.pool = [name for name in database.rooms.keys()]

        # #add more green room
        # self.pool.extend([name for name, data in database.rooms.items() if data['color'] == 'green'])
        # #add more orange room
        # self.pool.extend([name for name, data in database.rooms.items() if data['color'] == 'orange'])

        return self.pool

    def item_randmon_room(self, room_name, x, y):
        """ add random items in rooms_inventory """
        from navigation import Nav

        rarity_weights = {
            "coin": 20,
            "gem": 20,
            "key": 20,
            "apple": 20,
            "dice": 10,
            "Shovel": 2,
            "Lockpick_Kit": 2,
            'Lucky_Rabbits_Foot': 2,
            "Power_Hammer": 2,
            "Metal_Detector":2,
            "coffer": 1
        }
        rarity_weights_green = {
            "coin": 40,
            "gem": 40,
            "key": 40,
            "apple": 40,
            "dice": 20,
            "Shovel": 10,
            "Lockpick_Kit": 10,
            'Lucky_Rabbits_Foot': 0,
            "Power_Hammer": 10,
            "Metal_Detector":10,
            "coffer":5
        }
        
        if "Metal_Detector" in Nav.inventory.permanents:
            rarity_weights["key"] = 40
            rarity_weights["coin"] = 40
            rarity_weights["Shovel"] = 4
            rarity_weights["Lockpick_Kit"] = 4
            rarity_weights["Metal_Detector"] = 0
            rarity_weights_green["key"] = 50
            rarity_weights_green["coin"] = 50
            rarity_weights_green["Shovel"] = 15
            rarity_weights_green["Lockpick_Kit"] = 15
            rarity_weights_green["Metal_Detector"] = 0

            
        self.effect_6 = False #modified in navigatio.py and in the class effect

        if ((self.effect_6 and database.rooms[room_name]['color'] == 'green') or ("Lucky_Rabbits_Foot" in Nav.inventory.permanents)):

            item_pool_green = [0]*400
            for name, weight in rarity_weights_green.items():
                item_pool_green.extend([name] * weight)
            
            for _ in range(4):
                rand_index = rd.randint(0,len(item_pool_green)-1)
                act_item = item_pool_green[rand_index]

                if act_item in ["Shovel", "Lockpick_Kit"] and self.rooms_inventory[x][y][act_item] > 0:
                    continue

                if item_pool_green[rand_index] != 0:
                    self.rooms_inventory[x][y][act_item] += 1
            

        else:
            item_pool = [0]*400
            
            for name, weight in rarity_weights.items():
                item_pool.extend([name] * weight)
            
            for _ in range(4):
                rand_index = rd.randint(0,len(item_pool)-1)
                act_item = item_pool[rand_index]

                if act_item in ["Shovel", "Lockpick_Kit"] and self.rooms_inventory[x][y][act_item] > 0:
                    continue

                if item_pool[rand_index] != 0:
                    self.rooms_inventory[x][y][act_item] += 1
        
            


    def update_proba_pool(self):
        self.proba_pool = []

        rarity_weights = {
            -1: 0,   # unused
            0: 27,   # common
            1: 9,    # standard
            2: 3,    # unusual
            3: 1     # rare
        }
        for name in self.pool:
            data = database.rooms[name]
            rarity = data["rarity"]
            weight = rarity_weights.get(rarity, 0)
            if weight > 0:
                self.proba_pool.extend([name] * weight)

        return self.proba_pool

    @staticmethod
    def rot_doors(room, n=1):
        """
        Rotate the door list n times
        
        Example:
            Input : [1, 2, 3, 4], n=1 → [4, 1, 2, 3]
            Input : [1, 2, 3, 4], n=2 → [3, 4, 1, 2]
        """
        n = n % len(room)  #protection overflow 
        return room[-n:] + room[:-n]
    
    def doors_layout(self, room_doors, x, y, player_r):
        """
        doors = [bottom, right, top, left]
        0 : if no door
        1 : if door
        Return  True if the doors can be placed in the position x, y
                and the rotation of the future room
        """
        allowed_doors = [-1, -1, -1, -1]

        #Check walls
        if x == 0:
            allowed_doors[3] = 0
        if x == 4:
            allowed_doors[1] = 0
        if y == 0:
            allowed_doors[0] = 0
        if y == 8:
            allowed_doors[2] = 0
        
        #Unlock the front door
        front = (player_r+2) % 4 #Change the rotation to the front of the room
        allowed_doors[front] = 1

        # Test all 4 rotations in random order
        rotations = [0, 1, 2, 3]; rd.shuffle(rotations)
        for r in rotations:
            # Rotate the room's doors according to r
            rotated_doors = room_doors[:]

            rotated_doors = self.rot_doors(rotated_doors, r)

            # Check compatibility with allowed_doors
            doors_valid = True
            for allowed_door, door in zip(allowed_doors, rotated_doors):
                if allowed_door != -1 and allowed_door != door:
                    doors_valid = False
                    break

            if doors_valid:
                return True, r  # Found a valid rotation

        # If no valid rotation found      
        return False, None


    def level_up_door(self, doors, y):
        """
        Assigns a lock level (0, 1, 2, or 3) to each door based on progression through the mansion.

        Args:
            doors (list[int]): list of doors (e.g., [1, 1, 0, 1]) where 1 = existing door.
            y (int): current row index in the mansion.
        
        Returns:
            list[int]: updated list with door lock levels.
        """
        if y == 0:
            # First row → keep doors as they are (unlocked)
            return doors
        elif y == 8:   # last row
            # Last row → all existing doors become level 3 (fully locked)
            return [3 if door != 0 else 0 for door in doors]
        
        new_doors = []
        # Difficulty below 1 slows down the lock progression
        difficulty = 0.6  # doors level up too fast without this factor
        p = y / 8 * difficulty 

        for d in doors:
            if d == 0:
                new_doors.append(0)
            else:
                r = rd.random()
                if r < 1 - p:
                    new_doors.append(1)   # low-level lock
                elif r < 1 - p / 2:
                    new_doors.append(2)   # medium lock
                else:
                    new_doors.append(3)   # high-level lock

        return new_doors

    def block_door(self, doors, x, y):
        """
        Args:
            doors (list[int]): list of doors (e.g., [1, 1, 0, 1]) where 1 = existing door.
            x (int): current colomn index in the mansion.
            y (int): current row index in the mansion.
        
        Returns:
            list[int]: updated list with door blocked if wall from a room near the location
            and block the door of the room near the location
        """
        # Neighboring rooms ordered as [up, left, right, down]
        near_rooms = [
            [x, y - 1],    # down
            [x + 1, y],   # right
            [x, y + 1],   # up
            [x - 1, y]   # left
        ]

        new_doors = doors[:]
        

        for room_r, (x_near, y_near) in enumerate(near_rooms):
            in_map = (0 <= x_near < 5) and (0 <= y_near < 9)
            if in_map :
                if self.room_exists(x_near, y_near):
                    room = self.rooms[x_near][y_near]

                    # ex: if the room_r is up look for the bottom door
                    rotation = (room_r + 2) % 4

                    #block door both ways
                    if room.doors[rotation] == 0:
                        new_doors[room_r] = 0
                    if doors[room_r] == 0 :
                        room.doors[rotation] = 0
        return new_doors
