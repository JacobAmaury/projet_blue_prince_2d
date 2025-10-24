import pygame


##private
class Image:
    ##constructors
    def __init__(self,loaded_image) : 
        self.loaded = loaded_image
        self.position = (0,0)

    @classmethod
    def from_path_no_convertion(cls,bg_path):
        return cls(pygame.image.load(bg_path))
    
    @classmethod
    def from_path(cls,bg_path):
        return cls(pygame.image.load(bg_path).convert())

    @classmethod
    def from_path_transparent(cls,bg_path):
        return cls(pygame.image.load(bg_path).convert_alpha())

    ##methods
    def smoothscale(self,W,H):
        self.scaled = pygame.transform.smoothscale(self.loaded,(W, H))
    def scale(self,W,H):
        self.scaled = pygame.transform.scale(self.loaded,(W, H))
    def set_position(self,x,y):
        self.position = x,y
    def image_blit(self,screen):
        screen.blit(self.scaled, self.position)  

##public
class loadScreen :
    @classmethod
    def __init__(cls,bg_path,logo_path):
        #load images : cannot convert before set_mode()
        cls.bg_image = Image.from_path_no_convertion(bg_path)
        cls.logo_image = Image.from_path_no_convertion(logo_path)

    @classmethod
    def convert_loaded(cls):
        #optimize blit
        cls.bg_image.loaded = cls.bg_image.loaded.convert()
        cls.logo_image.loaded= cls.logo_image.loaded.convert_alpha()

    @classmethod
    def build_and_blit(cls,W,H,font,screen):
        ##build_load_screen
        #images
        cls.bg_image.smoothscale(W,H)
        cls.logo_image.scale(W//3, H//3)
        cls.logo_image.set_position(W//3 - cls.logo_image.scaled.get_height()//2, H//20)    #get_width ?
        #text
        cls.text_rendered = font.render("Loading game ...", True, (255, 255, 255))
        cls.text_position = (W //2 - cls.text_rendered.get_width()//2, H * 0.95)

        ##blit_load_screen
        #create load_screen
        cls.bg_image.image_blit(screen)
        #Logo
        cls.logo_image.image_blit(screen)   
        #text
        screen.blit(cls.text_rendered, cls.text_position)
