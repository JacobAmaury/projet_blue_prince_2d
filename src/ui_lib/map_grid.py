import pygame
from .inventory_grid import Image

##private to ./
class map:
    @classmethod
    def set_grid(cls,W,H):
        map.step_y = H * 0.0959
        map.step_x = W * 0.054
        map.base_x = W * 0.1695 # center (left_corner) of map_grid
        map.base_y = H * 0.837  # bottom (up_corner) of map_grid

    @classmethod
    def get_position_case(cls,col,row):
        x = map.base_x + col * map.step_x   #left of case
        y = map.base_y - row * map.step_y   #top of case
        return x,y

class Room(Image,map) : #Room images
    def __init__(self):
        Image.__init__(self)
        self.rot = [None]*4 # rotations : [O°,90°,180°,-90°]    directly stores scaled images

## private to ../
class door(map):
    #Parameters :
    LENGTH = 40/100         # in step %
    THICKNESS = 6/100       # in step %

    @classmethod
    def build(cls,player_position_map):
        (row,col,rot) = player_position_map
        #rot in [0,3]
        length, thickness = cls.LENGTH, cls.THICKNESS
        x,y = cls.get_position_case(col,row)

        r = 1 - rot // 2
        if rot%2 == 0 : # if pair (0:bot or 2:top)
            length = int(length * cls.step_x)
            thickness = int(thickness * cls.step_y)
            x = x + (cls.step_x - length)//2    #centered
            w = length
            y = y + (cls.step_y - thickness)*r
            h = thickness
        else:
            length = int(length * cls.step_y)
            thickness = int(thickness * cls.step_x)
            y = y + (cls.step_y - length)//2    #centered
            h = length
            x = x + (cls.step_x - thickness)*r
            w = thickness
        cls.player_position =  pygame.Rect(x,y,w,h)

    @classmethod
    def draw(cls,screen):
        COLOR = (255,255,255)
        pygame.draw.rect(screen,COLOR,cls.player_position)