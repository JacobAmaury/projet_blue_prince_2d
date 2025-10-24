import pygame

from options import Options
from rooms_db import Rooms_db
from inventory import Inventory
from map import Map

from .images import Permanent, Consumable, Room

class Display:
    window_ratio = (16,9)

    #list : sets the order on screen
    consumable_images = [Consumable('steps'),Consumable('key'),Consumable('gem'),Consumable('coin'),Consumable('dice')]
    permanent_images = [
        Permanent('Shovel'),
        Permanent('Lockpick_Kit'),
        Permanent('Lucky_Rabbits_Foot'),
        Permanent('Metal_Detector'),
        Permanent('Power_Hammer')
        ]
    
    # dic : no pre-set order on screen
    room_images = {}

    def __init__(self):
        #import display_size
        self.desk_W, self.desk_H = pygame.display.get_desktop_sizes()[0]
        #set window_size based on default_window_size
        self.screen_set_size(Options.default_window_size)
        #text size
        self.font = pygame.font.Font(None, self.H // 25) 

    def screen_set_size(self,window_size):
        W,H = window_size
        self.W, self.H = W,H
        #if default_window_size > display_size
        if self.W > self.desk_W or self.H > self.desk_H :
            self.maximize_window_v1(self.desk_W,self.desk_H)
        #set window_size
        Options.window_size = (W,H)

    def maximize_window_v1(self,desk_w,desk_h):
        #maximize window to biggest size inferior to current, keeping window_ratio
        width,height = self.W, self.H
        while width > desk_w or height > desk_h :
            width -= self.window_ratio[0] ; height -= self.window_ratio[1]
        self.W, self.H = (width,height)

    def load_loadScreen_images(self):
        #load images : cannot convert before set_mode()
        #load_screen
        path = "../images/background/BluePrince_Start.jpg"
        self.bg_image_load = pygame.image.load(path)
        #Logo
        path = "../images/Logo_Blue_Prince.png"
        self.image_logo = pygame.image.load(path)

    def create_window(self):
        #window creation
        pygame.display.set_caption("Blue prince 2D")
        blueprince_icon = pygame.image.load("../images/blueprince_icon.jpeg")
        pygame.display.set_icon(blueprince_icon)
        self.screen = pygame.display.set_mode((self.W, self.H),pygame.RESIZABLE)

    def convert_loadScreen(self):
        self.bg_image_load = self.bg_image_load.convert()
        self.image_logo = self.image_logo.convert_alpha()

    def build_and_blit_loadScreen(self):
        ##build_load_screen
        W,H = self.W,self.H
        #load_screen
        self.bg_load = pygame.transform.smoothscale(self.bg_image_load,(W, H))
        self.bg_load_position = (0,0)
        #Logo
        self.logo = pygame.transform.scale(self.image_logo,(W//3, H//3))
        self.logo_position = (W//3 - self.logo.get_height()//2,H//20,)
        #text
        self.loading_text = self.font.render("Loading game ...", True, (255, 255, 255))
        self.text_position = (W //2 - self.loading_text.get_width()//2, H * 0.95)

        ##blit_load_screen
        #create load_screen
        self.screen.blit(self.bg_load, self.bg_load_position)   
        #Logo
        self.screen.blit(self.logo,self.logo_position )    
        #text
        self.screen.blit(self.loading_text, self.text_position)

    def load_images(self,event_listener):
        #background image
        path = "../images/background/bg_image.png"
        self.bg_image = pygame.image.load(path).convert()

        #consumables
        for imageC in self.consumable_images :
            path = "../images/items/consumables/"+ imageC.name +"_icon.png"
            imageC.loaded = pygame.image.load(path).convert_alpha()

        #permanent objects
        for imageC in self.permanent_images :
            path = "../images/items/permanant_objects/"+ imageC.name +"_White_Icon.png"
            imageC.loaded = pygame.image.load(path).convert_alpha()

        #rooms : import all rooms by names from Rooms_db.rooms
        for name,color in Rooms_db.rooms.items():
            path = "../images/rooms/"+ color +'/'+ name +'.png'
            self.room_images[name] = Room()
            self.room_images[name].loaded = pygame.image.load(path).convert()
            event_listener() #room loading may be long : handles user input

    def build_bg_screen(self):
        #bg_screen is invariant => don't recalcul when items change
        W, H = self.W,self.H
        #back ground image
        self.bg = pygame.transform.smoothscale(self.bg_image,(W, H))

        #build consumable images
        #size for consumable_images
        consumable_size = (H//20,H//20) #square
        for imageC in self.consumable_images:
            imageC.scaled = pygame.transform.scale(imageC.loaded,consumable_size)

    def blit_bg_screen(self):
        W, H = self.W,self.H
        #back ground image
        self.screen.blit(self.bg, (0,0))
        
        #consumables :responsive position
        Consumable.set_position(W,H)
        for id,imageC in enumerate(self.consumable_images):
            self.screen.blit(imageC.scaled, Consumable.get_position_img(id))    #issue with dice position
    
    def build_items(self):
        #consumable cpt 
        inventory_consumables = Inventory.consumables
        for consumable in self.consumable_images:
            consumable.txt = self.font.render(str(inventory_consumables[consumable.name]), True, (255, 255, 255))

        #permanent objects
        W, H = self.W,self.H
        perm_size = (W//11, H//11)
        for imageC in self.permanent_images :
            imageC.scaled = pygame.transform.scale(imageC.loaded,perm_size)

    def blit_items(self):
        W, H = self.W,self.H
        #consumable cpt 
        Consumable.set_position(W,H)
        for id,consumable in enumerate(self.consumable_images):
            self.screen.blit(consumable.txt, Consumable.get_position_txt(id))

        #We also can do a for loop for this
        perm_objects = Inventory.perm_objects
        if perm_objects['Shovel'] == True:
            self.screen.blit(self.permanent_images[0].scaled, (W * 0.58, H * 0.43))
        if perm_objects['Lockpick_Kit'] == True:
            self.screen.blit(self.permanent_images[1].scaled, (W * 0.68, H * 0.43))
        if perm_objects["Lucky_Rabbits_Foot"] == True:
            self.screen.blit(self.permanent_images[2].scaled, (W * 0.78, H * 0.43))
        if perm_objects['Metal_Detector'] == True:
            self.screen.blit(self.permanent_images[3].scaled, (W * 0.86, H * 0.43))
        if perm_objects['Power_Hammer'] == True:
            self.screen.blit(self.permanent_images[4].scaled, (W * 0.48, H * 0.53))

    def build_rooms(self):
        W, H = self.W, self.H
        # for rot = 0,2
        w_size = W // 18.5
        # h_size = W // 18.5            # if square => if bg_screen_H/bg_screen_W ratio constant
        h_size =  H // 10.40625         # screen 16:9 => 16/18.5 = 9/X => X = 9*18.5/16 = 10.40625
        for name, _ in Map.rooms.items():
            room_image = self.room_images[name]
            room_image.rot[0] = pygame.transform.scale(room_image.loaded, (w_size,h_size))
            room_image.rot[2] = pygame.transform.rotate(room_image.rot[0],90*2)
            im_temp = pygame.transform.scale(room_image.loaded, (h_size,w_size))    #due to bg_screen ratio variable
            room_image.rot[1] = pygame.transform.rotate(im_temp,90*1)
            room_image.rot[3] = pygame.transform.rotate(im_temp,90*3)

    def blit_rooms(self):
        W, H = self.W, self.H
        step_y = H * 0.0959
        step_x = W * 0.054
        base_x = W * 0.1695 # center (left_corner) of map_grid
        base_y = H * 0.837  # bottom (up_corner) of map_grid

        for name, position in Map.rooms.items():
            for row, col, angle in position:
                x = base_x + col * step_x
                y = base_y - row * step_y  
                self.screen.blit(self.room_images[name].rot[angle], (x, y))

    def build_door(self,row=0,col=0,rot=0):
        #rot in [0,3]
        #Paramètres :
        length = 40/100      # in step %
        thickness = 6/100  # in step %

        W, H = self.W, self.H
        step_y = H * 0.0959
        step_x = W * 0.054
        base_x = W * 0.1695 # center (left_corner) of map_grid
        base_y = H * 0.837  # bottom (up_corner) of map_grid
        x = base_x + col * step_x   #left of case
        y = base_y - row * step_y   #top of case

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
        self.door =  pygame.Rect(x,y,w,h)


    def draw_door(self):
        color = (255,0,0)
        pygame.draw.rect(self.screen,color,self.door)