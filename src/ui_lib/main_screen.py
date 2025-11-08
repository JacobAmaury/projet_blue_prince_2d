
from .window import Screen
from .image import ImageTransparant, ImageRoom, ImageFull
from .grids import Consumable_row, door, permanent_grid, map_grid
from .selection_menu import SelectionMenu
import database

class MainScreen(Screen) :

    def __init__(self,player):
        Screen.__init__(self)
        self.buffer = Screen.window.buffer
        self.player = player
        #import images from loadscreen
        self.bg_image = ImageFull(Screen.main_bg_img)
        self.consumable_rows = []  #list : order on screen
        for name,image in zip(database.consumables,Screen.consumable_imgs.values()):
            self.consumable_rows.append(Consumable_row(name,image))   #keep database order for display
        self.permanent_images = {}
        for name,image in Screen.permanant_imgs.items():
            self.permanent_images[name] = ImageTransparant(image)   # no preset order
        #display
        self.refresh()

    def set_all_relatives(self):
        """recalculates all the coordinates relatives to window.size"""
        W, H = self.size
        map_grid.set_grid(W,H)
        Consumable_row.set_grid(W,H)
        permanent_grid.set_grid(W,H)

    def refresh(self):
        self.build()
        self.blit()

    def build(self):
        self.size = self.window.size
        self.set_all_relatives()
        self.build_bg_screen()
        self.build_items()
        self.build_rooms()
        door.build(self.player.position)

    def blit(self):
        self.blit_bg_screen()
        self.blit_items() 
        self.blit_rooms()
        door.draw(self.buffer)

    ## updates
    def update_consumables(self):
        self.build_items()
        self.blit()

    def update_permanents(self):
        self.blit_items()
        self.blit() # overkill if we cannot lose a permanent object

    def update_map(self):
        self.build_rooms()
        self.blit() # overkill if we cannot remove a room

    def update_door(self):
        door.build(self.player.position)
        self.update_map()

    ## builds, blits
    def build_bg_screen(self):
        #bg_screen is invariant => don't recalcul when items change
        W, H = self.size
        #back ground image
        self.bg_image.scale((W, H))
        self.bg_image.position = (0,0)

        #scale all consumable images
        for id,consumable_row in enumerate(self.consumable_rows):
            consumable_row.scale_image()
            consumable_row.image.position = Consumable_row.get_position_img(id)

    def blit_bg_screen(self):
        buffer = self.buffer
        #back ground image
        self.bg_image.blit(buffer)
        
        #consumable images
        for consumable_row in self.consumable_rows:
            consumable_row.image.blit(buffer)

    def build_items(self):
        #consumable cpt 
        inventory_consumables = self.player.inventory.consumables
        for consumable_row in self.consumable_rows:
            consumable_row.render_txt(self.font,str(inventory_consumables[consumable_row.name]))

        #permanent objects
        for permanent_image in self.permanent_images.values() :
            permanent_grid.scale_image(permanent_image)

    def blit_items(self):
        #consumable cpt 
        for id,consumable_row in enumerate(self.consumable_rows):
            self.buffer.blit(consumable_row.txt, Consumable_row.get_position_txt(id))

        #permanents
        inv_permanents = self.player.inventory.permanents
        for id,name in enumerate(inv_permanents):
            self.buffer.blit(self.permanent_images[name].scaled, permanent_grid.get_position_img(id))

    def build_rooms(self):
        self.room_images = {}
        for col,col_rooms in enumerate(self.player.map.rooms):
            for row,room in enumerate(col_rooms):
                if room != 0 :
                    name = room.name
                    if name not in self.room_images :
                        room_image = ImageRoom(Screen.room_imgs[name])  #store only rooms in map
                        map_grid.scale_image(room_image)
                        room_image.positions.append((col,row,room.rotation))
                        self.room_images[name] = room_image
                    else:
                        self.room_images[name].positions.append((col,row,room.rotation))


    def blit_rooms(self):
        for room_image in self.room_images.values() :
            for position in room_image.positions :
                col,row,rot = position
                self.buffer.blit(room_image.scaled[rot], map_grid.get_position_case(col,row))


    ##selection menu
    def room_select_menu(self, rooms):
        """
        Display a selection menu for choosing one of three rooms.
        Returns the rank of the selected room, -1 if cancelled, 3 if reroll
        """ # what of the dice ? Why not return index ?
        menu =  SelectionMenu(rooms)
        self.window.ui.screen = menu    #set as current screen
        selected = menu.selection()
        self.window.ui.screen = self    #set as current screen
        self.blit()          # redraw main screen
        return selected

