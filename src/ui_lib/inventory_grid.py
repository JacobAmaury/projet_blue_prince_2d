
##private to file
class Image : #Loaded Image (without names)
    def __init__(self) : 
        self.loaded = None


class ImageCP(Image) : #consumable and permanent Image
    def __init__(self,name) :
        Image.__init__(self)
        self.name = name; self.scaled = None
    
##private to ./
class Permanent(ImageCP):
    def __init__(self,name) :
        ImageCP.__init__(self,name)

    @classmethod
    def set_grid(cls,W,H):
        # sets position of consumables from W,H
        cls.x = W * 0.483                #absolute position
        cls.y = H * 0.45
        cls.step_x = W * 0.095 
        cls.step_y = H * 0.10

    @classmethod
    def get_position_img(cls,rank):         #fills right to left, then hight to low
        rank = rank + 1                     # top_right corner unavailable
        x = (rank % 5) * cls.step_x + cls.x
        y = (rank // 5) * cls.step_y + cls.y
        #if rank == 1 : print(x,y)
        return x,y

class Consumable(ImageCP) :
    def __init__(self, name):
        ImageCP.__init__(self,name)
        self.txt = None

    @classmethod
    def set_grid(cls,W,H):
        # sets position of consumables from W,H
        cls.x =  W * 0.91                       #absolute position of consumables (upper left corner)
        cls.y = H * 0.13
        cls.txt_r_x = W * 0.035                 #relative position of text from each consumable
        cls.txt_r_y = H * 0.012
        cls.step_y = H * 0.044                  #relative y position of each consumable from the previous one

    @classmethod
    def get_position_img(cls,rank):
        return (cls.x,
                cls.y + cls.step_y * rank)
    
    @classmethod
    def get_position_txt(cls,rank):
        return (cls.x + cls.txt_r_x, 
                cls.y + cls.step_y * rank + cls.txt_r_y)
    

