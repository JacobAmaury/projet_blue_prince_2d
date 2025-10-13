from ui import UI

class Rooms :
    rooms = {
    "Mechanarium": [(1, 0),(2,-2)],
    "MusicRoom": [(2, 0)]
    }

    #names of pool are used yo load the room images
    pool = {
    "Mechanarium",
    "MusicRoom",
    "Security"}

    def add_room(name,position):
        if name in Rooms.rooms :
            Rooms.rooms[name] += [position]
        else:
            Rooms.rooms[name] = [position]
        UI.instance.update_map()
