
class Map :
    def __init__(self,ui):
        Map.ui = ui
        Map.rooms = { 'EntranceHall': [(0,0)] }

    def add_room(self,name,position):
        if name in Map.rooms :
            Map.rooms[name] += [position]
        else:
            Map.rooms[name] = [position]
        Map.ui.update_map()


    # rooms = {
    #     "Mechanarium": [(1, 0),(2,-2)],
    #     "MusicRoom": [(2, 0)]
    # }


    # pool = {}
