
class Map :
    @classmethod
    def __init__(cls,ui):
        Map.ui = ui
        Map.rooms = { 'EntranceHall': [(0,0,0)] }
        Map.door = (0,0,0)

    @classmethod
    def add_room(cls,name,position):
        y, x, r = position
        y = y % 9 ; x = x % 5 -2    #protection overflow (same in ui.update_door)
        r = r %4    #angle in [0;<4]
        if name in Map.rooms :
            Map.rooms[name] += [(y, x, r)]
        else:
            Map.rooms[name] = [(y, x, r)]
        Map.ui.update_map()

    @classmethod
    def move_door(cls,y,x,r):
        """(0,0,0) : (bottom,center,0°), rot:(0:0°,1:90°,2:180°,3:-90°)"""
        r = r % 4 ; y = y % 9 ; x = x % 5 -2    #protection overflow
        cls.door = (y,x,r)
        cls.ui.update_door()

