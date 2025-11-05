import database

class Player :
    def __init__(self,ui):
        Player.ui = ui
        self.map = Map()
        self.inventory = Inventory()

class Map :
    def __init__(self):
        self.rooms = { 'EntranceHall': [(0,0,0)] }
        self.player_position = (0,0,0)

    def rot_doors(self, room):
        """
        The last element of a list of door become the first 
        Input : [1, 2, 3, 4]
        Output : [4, 1, 2, 3]
        """
        rotated_room = [-1, -1, -1, -1]
        last_element = room[-1]
        rotated_room[1:] = room[:-1]
        rotated_room[0] = last_element
        return rotated_room

    def doors_layout(self, room_doors, x, y, player_r):
        """
        doors = [bottom, right, top, left]
        0 : if no door
        1 : if door
        Return  True if the doors can be placed in the position x, y
                and the rotation of the future room
        """
        doors = room_doors
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
        player_r = (player_r+2) % 4 #Change the player rotation to the front of the room
        allowed_doors[player_r] = 1


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

    def add_room(self,name,position):
        y, x, r = position
        r = r % 4; y = y % 9 ; x = (x+2) % 5 -2   #protection overflow

        if name in self.rooms :
            self.rooms[name] += [(y, x, r)]
        else:
            self.rooms[name] = [(y, x, r)]
        Player.ui.update_map()

    def move_player_position(self,y,x,r):
        """(0,0,0) : (bottom,center,0°), rot:(0:0°,1:90°,2:180°,3:-90°)"""
        r = r % 4 ; y = y % 9 ; x = (x+2) % 5 -2   #protection overflow 
        self.player_position = (y,x,r)
        Player.ui.update_player_position()

class Inventory:
    def __init__(self):
        self.consumables = {'steps': 70, 'coin': 0, 'gem': 2, 'key': 0, 'dice': 0}
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

