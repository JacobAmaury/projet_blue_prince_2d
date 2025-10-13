

class Rooms :
    rooms = {
    "Mechanarium": [(1, 0),(2,-2)],
    "MusicRoom": [(2, 0)],
    }

    #all the images are loaded in all_rooms (may change)
    all_rooms = {
    "Mechanarium": None,
    "MusicRoom": None,
    "Security": None}

    def update_rooms(ui):
        Rooms.rooms["Security"] = [(2, -1)]
        ui.change_map()
