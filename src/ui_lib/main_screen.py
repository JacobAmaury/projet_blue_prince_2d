import pygame

from .window import Screen
from .image import ImageRoom, ImageSimple, ImageReapeated
from .grids import Consumable_row, door, permanent_grid, map_grid
import database

class MainScreen(Screen) :
    SIZE_CURRENT_ROOM = 0.1823
    CURRENT_ROOM_POSITION = (0.3645,0.177)
    CURRENT_ROOM_MSG_SIZE = 1     #relative to FONT_SIZE
    CURRENT_ROOM_MSG_POSITION = (0.665,0.77)  #center of text
    DOOR_POSITION = (0.38,0.762)
    DOOR_SIZE = 0.09
    KEY_SIZE = DOOR_SIZE / 2
    #screen print
    MSG_SIZE = 0.95     #relative to FONT_SIZE
    MSG_POSITION = (0.727,0.22)    #center_position

    def __init__(self,player):
        Screen.__init__(self)
        self.buffer = Screen.window.buffer
        self.player = player
        #import images from loadscreen
        self.bg_image = ImageSimple(Screen.main_bg_img)
        Screen.consumable_rows = []  #list : order on screen
        for name,image in zip(database.consumables,Screen.consumable_imgs.values()):
            Screen.consumable_rows.append(Consumable_row(name,image))   #keep database order for display
        self.permanent_images = {}
        for name,image in Screen.permanant_imgs.items():
            self.permanent_images[name] = ImageSimple(image)   # no preset order
        self.front_door_image = ImageSimple(Screen.front_door_img)
        self.closed_door_image = ImageSimple(Screen.closed_door_img)
        self.opened_door_image = ImageSimple(Screen.opened_door_img)
        self.plant_image = ImageSimple(Screen.plant_img)
        self.key_image = ImageReapeated(Screen.consumable_imgs['key'])
        self.key_image.positions = [None]*3
        #display
        self.update()

    def update(self):
        self.build()
        self.blit()

    def build(self):
        self.size = self.window.size
        w,h = self.size
        f = self.FONT_SIZE
        #set fonts
        txt_size = f * self.MSG_SIZE
        self.msg = pygame.font.SysFont(self.FONT, int(h * txt_size))
        self.msg.italic = True
        txt_size = f * self.CURRENT_ROOM_MSG_SIZE
        self.room_msg_font = pygame.font.SysFont(self.FONT, int(h * txt_size))
        self.font = pygame.font.Font(None, int(0.045*h) )
        self.set_all_relatives()
        self.build_bg_screen()
        self.build_items()
        self.build_rooms()
        door.build(self.player.position)
        self.build_current_room()
        self.build_door_status()

    def blit(self):
        self.blit_bg_screen()
        self.blit_items() 
        self.blit_rooms()
        door.draw(self.buffer)
        self.blit_status()

    def screen_print(self,msg):
        txt = self.msg.render(msg, True, (255, 255, 255))
        X, Y = self.MSG_POSITION ; w, h = self.size ; txt_w, txt_h = txt.get_size()
        position = (X*w - txt_w/2, Y*h + txt_h/2 )
        self.buffer.blit(txt, position)

    
## updates
    def set_all_relatives(self):
        """recalculates all the coordinates relatives to window.size"""
        W, H = self.size
        map_grid.set_grid(W,H)
        Consumable_row.set_grid(W,H)
        permanent_grid.set_grid(W,H)

    def update_consumables(self):
        self.build_items()
        self.blit()

    def update_permanents(self):
        self.blit_items()
        self.blit() # overkill if we cannot lose a permanent object

    def update_map(self):
        self.build_rooms()
        self.blit() # overkill if we cannot remove a room

    def update_player_position(self):
        door.build(self.player.position)
        self.build_current_room()
        self.update_map()


## builds, blits
    def build_bg_screen(self):
        #bg_screen is invariant => don't recalcul when items change
        W, H = self.size
        #back ground image
        self.bg_image.smoothscale((W, H))
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
                if room is not None :
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


    def build_current_room(self):
        w,h = self.size
        #build current room
        SIZE = self.SIZE_CURRENT_ROOM
        X,Y = self.CURRENT_ROOM_POSITION
        x,y,_ = self.player.position
        current_room_image = ImageSimple(Screen.room_imgs[self.player.map.rooms[x][y].name])
        current_room_image.smoothscale((SIZE * w, SIZE * h * 16/9))
        current_room_image.position = (X * w, Y * h)
        self.current_room_image = current_room_image
        #build enter_message
        X,Y = self.CURRENT_ROOM_MSG_POSITION
        current_room_txt = self.player.map.rooms[x][y].message
        if current_room_txt is not None:
            current_room_txt = self.room_msg_font.render(str(current_room_txt), True, (255, 255, 255))
            txt_w,txt_h = current_room_txt.get_size()
            self.current_room_txt_position = (X*w - txt_w/2, Y*h + txt_h/2)
        self.current_room_txt = current_room_txt

    def build_door_status(self):
        w,h = self.size
        # build all door_status images
        DOOR_X,DOOR_Y = self.DOOR_POSITION; DOOR_SIZE = self.DOOR_SIZE; KEY_SIZE = self.KEY_SIZE
        #plant
        image = self.plant_image
        image.smoothscale((DOOR_SIZE*0.7 * w, DOOR_SIZE*0.7 * h * 16/9))
        offset_x = DOOR_SIZE/2 - DOOR_SIZE*0.7/2
        offset_y = DOOR_SIZE - DOOR_SIZE*0.7
        image.position = ((DOOR_X + offset_x) * w, (DOOR_Y + offset_y * 16/9)* h)
        self.plant_image = image
        #front_door
        image = self.front_door_image
        image.smoothscale((DOOR_SIZE * w, DOOR_SIZE * h * 16/9))
        image.position = (DOOR_X * w, DOOR_Y * h)
        self.front_door_image = image
        #opened_door
        image = self.opened_door_image
        image.smoothscale((DOOR_SIZE * w, DOOR_SIZE * h * 16/9))
        image.position = (DOOR_X * w, DOOR_Y * h)
        self.opened_door_image = image
        #closed door
        image = self.closed_door_image
        image.smoothscale((DOOR_SIZE * w, DOOR_SIZE * h * 16/9))
        image.position = (DOOR_X * w, DOOR_Y * h)
        self.closed_door_image = image
        #key_0 image
        image = self.key_image
        offset = DOOR_SIZE/2 - KEY_SIZE/2
        image.scale((KEY_SIZE * w, KEY_SIZE * h * 16/9))
        image.positions[0] = ((DOOR_X + offset) * w,(DOOR_Y + offset*16/9) * h)
        #key1-2
        offset_y1 = offset - DOOR_SIZE/6
        offset_y2 = offset + DOOR_SIZE/6
        image.positions[1] = ((DOOR_X + offset) * w,(DOOR_Y + offset_y1*16/9) * h)
        image.positions[2] = ((DOOR_X + offset) * w,(DOOR_Y + offset_y2*16/9) * h)
        self.key_image = image

    def blit_status(self):
        buffer = self.buffer
        #blit current room
        self.current_room_image.blit(buffer)
        if self.current_room_txt is not None:
            buffer.blit(self.current_room_txt,self.current_room_txt_position)
        # blit current doom_status
        door_status = self.player.door_status
        if door_status == -2 :      #front door
            self.front_door_image.blit(buffer)
        elif door_status == -1 :    #opened door
            self.opened_door_image.blit(buffer)
        elif door_status == 0:      #wall
            self.plant_image.blit(buffer)
        elif door_status > 0 :      #closed door
            self.closed_door_image.blit(buffer)
            if door_status == 2 :   #locked1 door
                self.key_image.blit_single(buffer,0)
            elif door_status == 3:  #locked2 door
                self.key_image.blit_single(buffer,1)
                self.key_image.blit_single(buffer,2)
