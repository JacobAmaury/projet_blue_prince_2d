


class Image : #Loaded Image (without names)
    def __init__(self) : 
        self.loaded = None

class BackGround(Image):
    def __init__(self) : 
        self.loaded = None

class Room(Image) : #Room images
    def __init__(self):
        Image.__init__(self)
        self.rot = [None]*4 # rotations : [O°,90°,180°,-90°]    directly stores scaled images

class ImageCP(Image) : #consumable and permanent Image
    def __init__(self,name) :
        Image.__init__(self)
        self.name = name; self.scaled = None

class Permanent(ImageCP):
    def __init__(self,name) :
        ImageCP.__init__(self,name)

class Consumable(ImageCP) :
    x, y = None,None                    #absolute position of consumablesRect (upper left corner)
    r_y = None                          #relative y position of each consumableRect from the previous one
    txt_r_x,  txt_r_y = None, None      #relative position of text from each consumableRect
    def __init__(self, name):
        ImageCP.__init__(self,name)
        self.txt = None

    def set_position(W,H):
        # sets position of consumablesRect from W,H
        Consumable.x, Consumable.y = W * 0.91, H * 0.13
        Consumable.txt_r_x, Consumable.txt_r_y = W * 0.035, H * 0.01
        Consumable.r_y = H * 0.045

    def get_position_img(rank):
        return (Consumable.x,
                Consumable.y + Consumable.r_y * rank)
    
    def get_position_txt(rank):
        return (Consumable.x + Consumable.txt_r_x, 
                Consumable.y + Consumable.r_y * rank + Consumable.txt_r_y)
    
