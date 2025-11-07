import database
import random as rd

class Player :
    def __init__(self,ui):
        Player.ui = ui
        self.map = Map()
        self.inventory = Inventory()

    def move_player_position(self,y,x,r):
        """(0,0,0) : (bottom,center,0°), rot:(0:0°,1:90°,2:180°,3:-90°)"""
        r = r % 4 ; y = y % 9 ; x = (x+2) % 5 -2   #protection overflow 
        self.map.player_position = (y,x,r)
        Player.ui.update_player_position()

    def game_won(self):
        print("You won!!!")
        Player.ui.quit_game()

    def game_over(self):
        print("You lost...")
        Player.ui.quit_game()


class Map :
    def __init__(self):
        self.rooms = { 'EntranceHall': [(0,0,0)] } #y, x
        self.doors_map = [[[] for y in range(9)] for x in range(5)]  #x, y, doors[]
        self.doors_map[2][0] = [0, 1, 1, 1]
        self.player_position = (0,0,0)
        self.rooms_inventory =  [[{
            "coin": 0,
            "gem": 0,
            "key": 0,
            "dice": 0,
            "apple":0,
            "Shovel": 0,
            "Lockpick_Kit": 0
        } for y in range(9)] for x in range(5)]  #x, y, database_element

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

        self.effect_6 = False #modified in navigatio.py and in the class effect

        if (self.effect_6) and (database.rooms[room_name]['color'] == 'green'):
            item_pool_green = [0]*50
            rarity_weights_green = {
                "coin": 40,
                "gem": 40,
                "key": 40,
                "apple": 40,
                "dice": 20,
                "Shovel": 10,
                "Lockpick_Kit": 10
            }
            
            for name, weight in rarity_weights.items():
                item_pool_green.extend([name] * weight)
            
            for _ in range(4):
                rand_index = rd.randint(0,len(item_pool)-1)
                act_item = item_pool_green[rand_index]

                if act_item in ["Shovel", "Lockpick_Kit"] and self.rooms_inventory[x][y][act_item] > 0:
                    continue

                if item_pool[rand_index] != 0:
                    self.rooms_inventory[x][y][act_item] += 1
            

        else:
            item_pool = [0]*50
            rarity_weights = {
                "coin": 20,
                "gem": 20,
                "key": 20,
                "apple": 20,
                "dice": 10,
                "Shovel": 2,
                "Lockpick_Kit": 2
            }
            
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


    def rot_doors(self, room, nb_rotation=1):
        """
        The last element of a list of door become the first 
        Input : [1, 2, 3, 4]
        Output : [4, 1, 2, 3]
        """
        if nb_rotation == 0:
            return room

        for _ in range(nb_rotation):
            rotated_room = [-1, -1, -1, -1]
            last_element = room[-1]
            rotated_room[1:] = room[:-1]
            rotated_room[0] = last_element

        return rotated_room

    # def doors_layout(self, room_doors, x, y, player_r):
    #     """
    #     doors = [bottom, right, top, left]
    #     0 : if no door
    #     1 : if door
    #     Return  True if the doors can be placed in the position x, y
    #             and the rotation of the future room
    #     """
    #     allowed_doors = [-1, -1, -1, -1]

    #     #Check walls
    #     if x == -2:
    #         allowed_doors[3] = 0
    #     if x == 2:
    #         allowed_doors[1] = 0
    #     if y == 0:
    #         allowed_doors[0] = 0
    #     if y == 8:
    #         allowed_doors[2] = 0
        
    #     #Unlock the front door
    #     front = (player_r+2) % 4 #Change the rotation to the front of the room
    #     allowed_doors[front] = 1

    #     # Test all 4 rotations in random order
    #     rotations = [0, 1, 2, 3]; rd.shuffle(rotations)
    #     for r in rotations:
    #         # Rotate the room's doors according to r
    #         rotated_doors = room_doors[:]
    #         rotated_doors = self.rot_doors(rotated_doors, nb_rotation=r)

    #         # Check compatibility with allowed_doors
    #         doors_valid = True
    #         for allowed_door, door in zip(allowed_doors, rotated_doors):
    #             if allowed_door != -1 and allowed_door != door:
    #                 doors_valid = False
    #                 break

    #         if doors_valid:
    #             return True, r  # Found a valid rotation

    #     # If no valid rotation found
    #     return False, None
    
    def doors_layout(self, room_doors, x, y, player_r):
        """
        doors = [bottom, right, top, left]
        0 : if no door
        1 : if door
        Return  True if the doors can be placed in the position x, y
                and the rotation of the future room
        """
        doors = room_doors[:]
        allowed_doors = [-1, -1, -1, -1]

        #Check walls
        if x == -2:
            allowed_doors[3] = 0
        if x == 2:
            allowed_doors[1] = 0
        if y == 0:
            allowed_doors[0] = 0
        if y == 8:
            allowed_doors[2] = 0
        
        #Unlock the front door
        front = (player_r+2) % 4 #Change the rotation to the front of the room
        allowed_doors[front] = 1


        for r in range(4): #test 4 rotation
            doors_valid = True
            for allowed_door, door in zip(allowed_doors, doors):
                if (allowed_door != -1):
                    if (allowed_door != door):
                        doors_valid = False
                        break
            if doors_valid:
                break
            else: 
                doors = self.rot_doors(doors)
        return doors_valid, r

    def add_room(self,name,position, doors):
        y, x, r = position
        r = r % 4; y = y % 9 ; x = (x+2) % 5 -2   #protection overflow

        if name in self.rooms :
            self.rooms[name] += [(y, x, r)]
        else:
            self.rooms[name] = [(y, x, r)]

        index_x = x + 2
        self.doors_map[index_x][y] = doors 
        
        Player.ui.update_map()

class Inventory:
    def __init__(self):
        self.consumables = {'steps': 70, 'coin': 0, 'gem': 40, 'key': 0, 'dice': 0}
        self.permanents = []    #sets display order


    def change_consumable(self,name,increment):
        self.consumables[name] += increment
        Player.ui.update_consumables()

    def add_permanent(self,name):
        if name not in database.permanents :
            raise ValueError('name not in database')
        self.permanents.append(name)
        Player.ui.update_permanents()

    def remove_permanent(self,name):
        if name not in database.permanents :
            raise ValueError('name not in database')
        self.permanents.remove(name)
        Player.ui.update_permanents()

    def change_perm(self,name,isinside):
        if name not in database.permanents :
            raise ValueError('name not in database')
        if isinside:
            self.permanents.append(name)
        else :
            self.permanents.remove(name)
        Player.ui.update_permanents()

