import pygame
from .image import ImageSimple


class Consumable_row :
    TEXT_COLOR = (255, 255, 255)
    def __init__(self, name,image):
        self.name = name
        self.image = ImageSimple(image)
        self.txt = None
    
    def render_txt(self,font,msg):
        self.txt = font.render(msg, True, self.TEXT_COLOR)
    
    def scale_image(self):
        self.image.scale(self.consumable_size)

    @classmethod
    def set_grid(cls,W,H):
        # sets position of consumables from W,H
        cls.x =  W * 0.91                       #absolute position of consumables (upper left corner)
        cls.y = H * 0.13
        cls.txt_r_x = W * 0.03                 #relative position of text from each consumable
        cls.txt_r_y = H * 0.01
        cls.step_y = H * 0.046                  #relative y position of each consumable from the previous one
        cls.consumable_size = (H//22,H//22)

    @classmethod
    def get_position_img(cls,rank):
        return (cls.x,
                cls.y + cls.step_y * rank)
    
    @classmethod
    def get_position_txt(cls,rank):
        return (cls.x + cls.txt_r_x, 
                cls.y + cls.step_y * rank + cls.txt_r_y)
    

class permanent_grid:
    @classmethod
    def scale_image(cls,image):
        image.scale(cls.perm_size)

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

class map_grid:
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
    
    @classmethod
    def scale_image(cls,room_image):
        room_image.scale(cls.room_size)


class door:
    #Parameters :
    LENGTH = 40/100         # in step %
    THICKNESS = 6/100       # in step %

    @classmethod
    def build(cls,position):
        (col,row,rot) = position
        step_x, step_y = map_grid.step_x, map_grid.step_y
        length, thickness = cls.LENGTH, cls.THICKNESS
        x,y = map_grid.get_position_case(col,row)

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