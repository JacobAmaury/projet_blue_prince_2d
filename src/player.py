import database
class Player :
    def __init__(self,ui):
        Player.ui = ui
        self.map = Map()
        self.inventory = Inventory()

class Map :
    def __init__(self):
        self.rooms = { 'EntranceHall': [(0,0,0)] }
        self.door = (0,0,0)

    def add_room(self,name,position):
        y, x, r = position
        y = y % 9 ; x = (x+2) % 5 -2   #protection overflow (same in ui.update_door)
        r = r %4    #angle in [0;<4]
        if name in self.rooms :
            self.rooms[name] += [(y, x, r)]
        else:
            self.rooms[name] = [(y, x, r)]
        Player.ui.update_map()

    def move_door(self,y,x,r):
        """(0,0,0) : (bottom,center,0°), rot:(0:0°,1:90°,2:180°,3:-90°)"""
        r = r % 4 ; y = y % 9 ; x = (x+2) % 5 -2   #protection overflow 
        self.door = (y,x,r)
        Player.ui.update_door()

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

