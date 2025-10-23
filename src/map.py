
class Map :
    def __init__(self,ui):
        Map.ui = ui
        Map.rooms = { 'EntranceHall': [(0,0,0)] }

    def add_room(self,name,position):
        x, y, a = position
        a = a %4    #angle in [0;<4]
        if name in Map.rooms :
            Map.rooms[name] += [(x, y, a)]
        else:
            Map.rooms[name] = [(x, y, a)]
        Map.ui.update_map()


