
class Map :
    def __init__(self,ui):
        self.ui = ui
        self.rooms = { 'EntranceHall': [(0,0)] }

    def add_room(self,name,position):
        if name in self.rooms :
            self.rooms[name] += [position]
        else:
            self.rooms[name] = [position]
        self.ui.update_map()


    # rooms = {
    #     "Mechanarium": [(1, 0),(2,-2)],
    #     "MusicRoom": [(2, 0)]
    # }


    # pool = {}
