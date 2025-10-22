from ui import UI

class Map :
    rooms = {
        'EntranceHall': [(0,0)],
        "Mechanarium": [(1, 0),(2,-2)],
        "MusicRoom": [(2, 0)]
    }


    pool = {}

    def add_room(name,position):
        if name in Map.rooms :
            Map.rooms[name] += [position]
        else:
            Map.rooms[name] = [position]
        UI.instance.update_map()
