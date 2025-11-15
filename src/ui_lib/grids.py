import pygame
from .image import ImageSimple, ImageRoom
from .window import Screen
import database


class Consumable_grid :
    TEXT_COLOR = (255, 255, 255)
    POSITION = (0.91, 0.13) #relative to screen.size
    TXT_OFFSET = (0.03, 0.01)
    STEP = 0.046    #relative to screen.size.h
    SIZE_TEXT = 0.045

    def __init__(self):
        self.names = []
        self.images = []
        imgs = Screen.consumable_imgs
        for name in database.consumables: #in order set in database for display
            self.names.append(name)
            self.images.append(ImageSimple(imgs[name]))
        self.texts = [None]*len(self.names)
    
    def render_txt(self,font,msg):
        self.txt = font.render(msg, True, self.TEXT_COLOR)
    
    def scale_images(self):
        for id,image in enumerate(self.images):
            image.scale(self.consumable_size)
            image.position = self.get_position_img(id)

    def build_text(self,player):
        self.font = pygame.font.Font(None, self.size_text)
        #consumable cpt 
        inventory_consumables = player.inventory.consumables
        font = self.font
        for id,name in enumerate(self.names):
            msg = str(inventory_consumables[name])
            self.texts[id] = font.render(msg, True, self.TEXT_COLOR)

    def blit_images(self,buffer):
        for image in self.images:
            image.blit(buffer)

    def blit_text(self,buffer):
        for id,text in enumerate(self.texts):
            buffer.blit(text, self.get_position_txt(id))

    @classmethod
    def set_grid(cls,w,h):
        # sets position of consumables from W,H
        X,Y = cls.POSITION
        TXT_X, TXT_Y = cls.TXT_OFFSET
        cls.x =  w * X                       #absolute position of consumables (upper left corner)
        cls.y = h * Y
        cls.txt_r_x = w * TXT_X                 #relative position of text from each row
        cls.txt_r_y = h * TXT_Y
        cls.step_y = h * cls.STEP                  #relative y position of each row from the previous one
        cls.consumable_size = (h//22,h//22)
        cls.size_text = int(cls.SIZE_TEXT * h)

    @classmethod
    def get_position_img(cls,rank):
        return (cls.x,
                cls.y + cls.step_y * rank)
    
    @classmethod
    def get_position_txt(cls,rank):
        return (cls.x + cls.txt_r_x, 
                cls.y + cls.step_y * rank + cls.txt_r_y)
    



class Permanent_grid:
    def __init__(self):
        self.images = {}
        for name,image in Screen.permanant_imgs.items():
            self.images[name] = ImageSimple(image)   # no preset order

    def scale_images(self):
        for image in self.images.values() :
            image.scale(self.perm_size)

    def blit_images(self,buffer,player):
        inv_permanents = player.inventory.permanents
        for id,name in enumerate(inv_permanents):
            buffer.blit(self.images[name].scaled, self.get_position_img(id))

    @classmethod
    def set_grid(cls,W,H):
        # sets position of consumables from W,H
        cls.x = W * 0.483                #absolute position
        cls.y = H * 0.45
        cls.step_x = W * 0.095 
        cls.step_y = H * 0.10
        cls.perm_size = (W//11, H//11)

    @classmethod
    def get_position_img(cls,rank):         #fills right to left, then hight to low
        rank = rank + 1                     # top_right corner unavailable
        x = (rank % 5) * cls.step_x + cls.x
        y = (rank // 5) * cls.step_y + cls.y
        #if rank == 1 : print(x,y)
        return x,y

class Map_grid:
    def __init__(self):
        self.room_images = {}
    
    def build_rooms(self,player):
        self.room_images = {}
        for col,col_rooms in enumerate(player.map.rooms):
            for row,room in enumerate(col_rooms):
                if room is not None :
                    name = room.name
                    if name not in self.room_images :
                        room_image = ImageRoom(Screen.room_imgs[name])  #store only rooms in map
                        room_image.scale(self.room_size)
                        room_image.positions.append((col,row,room.rotation))
                        self.room_images[name] = room_image
                    else:
                        self.room_images[name].positions.append((col,row,room.rotation))
    
    def blit_rooms(self,buffer):
        for room_image in self.room_images.values() :
            for position in room_image.positions :
                col,row,rot = position
                buffer.blit(room_image.scaled[rot], Map_grid.get_position_case(col,row))

    @classmethod
    def set_grid(cls,W,H):
        cls.step_y = H * 0.0965 #0.0959
        cls.step_x = W * 0.054
        cls.base_x = W * 0.0615 #0.1695 # left of map_grid
        cls.base_y = H * 0.837  # bottom (up_corner) of map_grid
        #room size for rotations 0 and 2 (invert h and w for 1 and 3)
        cls.room_size = (int(W * 0.0547), int(H * 0.0547 * 16/9))   #0.0540

    @classmethod
    def get_position_case(cls,col,row):
        x = cls.base_x + col * cls.step_x   #left of case
        y = cls.base_y - row * cls.step_y   #top of case
        return x,y

class door:
    #Parameters :
    LENGTH = 40/100         # in step %
    THICKNESS = 6/100       # in step %

    @classmethod
    def build(cls,position):
        (col,row,rot) = position
        step_x, step_y = Map_grid.step_x, Map_grid.step_y
        length, thickness = cls.LENGTH, cls.THICKNESS
        x,y = Map_grid.get_position_case(col,row)

        r = 1 - rot // 2
        if rot%2 == 0 : # if pair (0:bot or 2:top)
            length = int(length * step_x)
            thickness = int(thickness * step_y)
            x = x + (step_x - length)//2    #centered
            w = length
            y = y + (step_y - thickness)*r
            h = thickness
        else:
            length = int(length * step_y)
            thickness = int(thickness * step_x)
            y = y + (step_y - length)//2    #centered
            h = length
            x = x + (step_x - thickness)*r
            w = thickness
        cls.door =  pygame.Rect(x,y,w,h)

    @classmethod
    def draw(cls,screen):
        COLOR = (255,255,255)
        pygame.draw.rect(screen,COLOR,cls.door)