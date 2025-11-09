import pygame

class Image:    #abstract
    #constructors
    def __init__(self,loaded_image) : 
        self.loaded = loaded_image

    #methods
    def scale(self,size):    #abstract
        pass
    #def blit abstract ?

    #static
    @staticmethod
    def loadFull(path):
        return pygame.image.load(path).convert()

    @staticmethod
    def loadTransparent(path):
        return pygame.image.load(path).convert_alpha()



class ImageSimple(Image):
    def __init__(self,loaded_image) : 
        Image.__init__(self,loaded_image)
        self.scaled = None
        self.position = None
    
    def smoothscale(self,size):
        self.scaled = pygame.transform.smoothscale(self.loaded,size)

    def scale(self,size):
        self.scaled = pygame.transform.scale(self.loaded,size)

    def blit(self,buffer):
        buffer.blit(self.scaled, self.position)  


class ImageReapeated(Image):    #abstract
    #constructors
    def __init__(self,loaded_image) : 
        Image.__init__(self,loaded_image)
        self.positions=[]
        self.scaled = None

    def scale(self,size):
        self.scaled = pygame.transform.scale(self.loaded,size)

    def blit_single(self,buffer,id):
        buffer.blit(self.scaled, self.positions[id])  



class ImageRoom(Image):    #reapeated and rotations
    def __init__(self,loaded_image):
        Image.__init__(self,loaded_image)
        self.positions=[]
        self.scaled = [None]*4  #[0:0°,1:90°,2,180°,3:-90°]
    
    def scale(self,room_size):
        (w_size,h_size) = room_size
        self.scaled[0] = pygame.transform.scale(self.loaded, (w_size,h_size))
        self.scaled[2] = pygame.transform.rotate(self.scaled[0],90*2)
        im_temp = pygame.transform.scale(self.loaded, (h_size,w_size))    #due to bg_screen ratio variable
        self.scaled[1] = pygame.transform.rotate(im_temp,90*1)
        self.scaled[3] = pygame.transform.rotate(im_temp,90*3)