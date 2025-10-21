from ui import UI

class Rooms :
    rooms = {
        'EntranceHall': [(0,0)],
        "Mechanarium": [(1, 0),(2,-2)],
        "MusicRoom": [(2, 0)]
    }


    pool = {}

    def add_room(name,position):
        if name in Rooms.rooms :
            Rooms.rooms[name] += [position]
        else:
            Rooms.rooms[name] = [position]
        UI.instance.update_map()
