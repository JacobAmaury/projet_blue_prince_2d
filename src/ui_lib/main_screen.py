import pygame

from .window import Screen
from .image import ImageRoom, ImageSimple, ImageReapeated
from .grids import Consumable_grid, door, Permanent_grid, Map_grid
import database

class MainScreen(Screen) :
    SIZE_CURRENT_ROOM = 0.1823
    CURRENT_ROOM_POSITION = (0.3645,0.177)
    CURRENT_ROOM_MSG_SIZE = 0.7     #relative to FONT_SIZE
    CURRENT_ROOM_MSG_POSITION = (0.665,0.805)  #center of text
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
        #grids
        Screen.consumable_grid = Consumable_grid()
        self.permanent_grid = Permanent_grid()
        self.map_grid = Map_grid()
        self.closed_door_image = ImageSimple(Screen.closed_door_img)
        self.opened_door_image = ImageSimple(Screen.opened_door_img)
        self.key_image = ImageReapeated(Screen.consumable_imgs['key'])
        self.key_image.positions = [None]*3
        #display
        self.update()

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
        self.set_all_relatives()
        self.build_bg_screen()
        self.build_items()
        self.map_grid.build_rooms(self.player)
        door.build(self.player.position)
        self.build_current_room()
        self.build_door_status()

    def blit(self):
        self.blit_bg_screen()
        self.blit_items() 
        self.map_grid.blit_rooms(self.buffer)
        door.draw(self.buffer)
        self.blit_status()

    def print(self,msg):
        txt = self.msg.render(msg, True, (255, 255, 255))
        X, Y = self.MSG_POSITION ; w, h = self.size ; txt_w, txt_h = txt.get_size()
        position = (X*w - txt_w/2, Y*h + txt_h/2 )
        self.buffer.blit(txt, position)
        pygame.display.flip()

    
## updates
    def set_all_relatives(self):
        """recalculates all the coordinates relatives to window.size"""
        W, H = self.size
        Map_grid.set_grid(W,H)
        Consumable_grid.set_grid(W,H)
        Permanent_grid.set_grid(W,H)

    def update_consumables(self):
        self.build_items()
        self.blit()

    def update_permanents(self):
        self.blit_items()
        self.blit() # overkill if we cannot lose a permanent object

    def update_map(self):
        self.map_grid.build_rooms(self.player)
        self.blit() # overkill if we cannot remove a room

    def update_player_position(self):
        door.build(self.player.position)
        self.build_current_room()
        self.update_map()

    def update_current_room(self):
        self.build_current_room()
        self.blit()


## builds, blits
    def build_bg_screen(self):
        #bg_screen is invariant => don't recalcul when items change
        W, H = self.size
        #back ground image
        self.bg_image.smoothscale((W, H))
        self.bg_image.position = (0,0)

        #scale all consumable images
        self.consumable_grid.scale_images()

    def blit_bg_screen(self):
        buffer = self.buffer
        #back ground image
        self.bg_image.blit(buffer)
        #consumable images
        self.consumable_grid.blit_images(buffer)

    def build_items(self):
        #consumable cpt 
        self.consumable_grid.build_text(self.player)
        #permanent objects
        self.permanent_grid.scale_images()

    def blit_items(self):
        buffer = self.buffer
        #consumable cpt 
        self.consumable_grid.blit_text(buffer)
        #permanents
        self.permanent_grid.blit_images(buffer,self.player)

    def build_current_room(self):
        w,h = self.size
        #build current room
        SIZE = self.SIZE_CURRENT_ROOM
        X,Y = self.CURRENT_ROOM_POSITION
        current_room_image = ImageSimple(Screen.room_imgs[self.player.current_room.name])
        current_room_image.smoothscale((SIZE * w, SIZE * h * 16/9))
        current_room_image.position = (X * w, Y * h)
        self.current_room_image = current_room_image
        #build enter_message
        X,Y = self.CURRENT_ROOM_MSG_POSITION
        current_room_txt = self.player.current_room.message
        if current_room_txt is not None:
            current_room_txt = self.room_msg_font.render(str(current_room_txt), True, (255, 255, 255))
            txt_w,txt_h = current_room_txt.get_size()
            self.current_room_txt_position = (X*w - txt_w/2, Y*h - txt_h/2)
        self.current_room_txt = current_room_txt

    def build_door_status(self):
        w,h = self.size
        # build all door_status images
        DOOR_X,DOOR_Y = self.DOOR_POSITION; DOOR_SIZE = self.DOOR_SIZE; KEY_SIZE = self.KEY_SIZE
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
        if door_status == 0 :   #wall
            return
        elif door_status == -1 :    #opened door
            self.opened_door_image.blit(buffer)
        elif door_status > 0 :      #closed door
            self.closed_door_image.blit(buffer)
            if door_status == 2 :   #locked1 door
                self.key_image.blit_single(buffer,0)
            elif door_status == 3:  #locked2 door
                self.key_image.blit_single(buffer,1)
                self.key_image.blit_single(buffer,2)