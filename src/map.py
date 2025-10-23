
class Map :
    def __init__(self,ui):
        Map.ui = ui
        Map.rooms = { 'EntranceHall': [(0,0,0)] }

    def add_room(self,name,position):
        y, x, r = position
        y = y % 9 ; x = x % 5 -2    #protection overflow (same in ui.update_door)
        r = r %4    #angle in [0;<4]
        if name in Map.rooms :
            Map.rooms[name] += [(y, x, r)]
        else:
            Map.rooms[name] = [(y, x, r)]
        Map.ui.update_map()


