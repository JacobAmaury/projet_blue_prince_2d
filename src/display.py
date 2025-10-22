import pygame

from options import Options
from rooms_db import Rooms_db
from inventory import Inventory
from map import Map


class Display:
    window_ratio = (16,9)
    consumable_images = {}  #loaded consumable images
    consumables_scaled = {}  #scaled consumable images
    permanents_images = {}  #loaded permanent objects images
    permanents_scaled = {}  #scaled permanent objects images
    room_images = {}    #loaded room images
    rooms_scaled = {}   #scaled room images

    def __init__(self):
        #import display_size
        self.desk_W, self.desk_H = pygame.display.get_desktop_sizes()[0]
        #set window_size based on default_window_size
        self.screen_set_size(Options.default_window_size)
        #text size
        self.font = pygame.font.Font(None, self.H // 25) 
        #load ressources for loadScreen
        self.load_loadScreen_images()

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

    def create_window(self):
        #window creation
        pygame.display.set_caption("Blue prince 2D")
        blueprince_icon = pygame.image.load("../images/blueprince_icon.jpeg")
        pygame.display.set_icon(blueprince_icon)
        self.screen = pygame.display.set_mode((self.W, self.H),pygame.RESIZABLE)

    def load_loadScreen_images(self):
        #load_screen
        path = "../images/background/BluePrince_Start.jpg"
        self.bg_image_load = pygame.image.load(path)
        #Logo
        path = "../images/Logo_Blue_Prince.png"
        self.image_logo = pygame.image.load(path)

    def build_and_blit_loadScreen(self):
        ##build_load_screen
        W,H = self.W,self.H
        #load_screen
        self.bg_load = pygame.transform.scale(self.bg_image_load,(W, H))
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

    def load_images(self,event_handler):
        #background image
        path = "../images/background/bg_image.png"
        self.bg_image = pygame.image.load(path)

        #consumables
        for name in Inventory.consumables :
            path = "../images/items/consumables/"+ name +"_icon.png"
            self.consumable_images[name] = pygame.image.load(path)

        #permanent objects
        for name in Inventory.perm_objects :
            path = "../images/items/permanant_objects/"+ name +"_White_Icon.png"
            self.permanents_images[name] = pygame.image.load(path)

        #rooms : import all rooms by name from Rooms_db.rooms
        for name,color in Rooms_db.rooms.items():
            path = "../images/rooms/"+ color +'/'+ name +'.png'
            self.room_images[name] = pygame.image.load(path)
            event_handler() #room loading may be long : handles user input

    def build_bg_screen(self):
        #bg_screen is invariant => don't recalcul when items change
        W, H = self.W,self.H
        #back ground image
        self.bg = pygame.transform.scale(self.bg_image,(W, H))

        #build consumable images
        #size for consumable_images
        consumable_size = (H//20,H//20)
        for name,img in self.consumable_images.items():
            self.consumables_scaled[name] = pygame.transform.scale(img,consumable_size)

    def blit_bg_screen(self):
        W, H = self.W,self.H
        #back ground image
        self.screen.blit(self.bg, (0,0))
        
        #responsive position
        self.screen.blit(self.consumables_scaled['steps'], (W * 0.91, H * 0.13))
        self.screen.blit(self.consumables_scaled['key'],   (W * 0.91, H * 0.18))
        self.screen.blit(self.consumables_scaled['gem'],   (W * 0.91, H * 0.23))  
        self.screen.blit(self.consumables_scaled['coin'],  (W * 0.91, H * 0.28)) 
        # screen.blit(self.consumables['dice'],  (W * 0.91, H * 0.)) #I don't kwon were it go
    
    def build_items(self):
        W, H = self.W,self.H
        perm_size = (W//11, H//11)
        #consumable cpt 
        consumables = Inventory.consumables
        self.text_step = self.font.render(str(consumables["steps"]), True, (255, 255, 255))
        self.text_key = self.font.render(str(consumables["key"]), True, (255, 255, 255))
        self.text_gem = self.font.render(str(consumables["gem"]), True, (255, 255, 255))
        self.text_coin = self.font.render(str(consumables["coin"]), True, (255, 255, 255))
    
        #permanent objects
        for name,img in self.permanents_images.items() :
            self.permanents_scaled[name] = pygame.transform.scale(img, perm_size)

    def blit_items(self):
        W, H = self.W,self.H
        #consumable cpt 
        self.screen.blit(self.text_step, (W * 0.94, H * 0.14))
        self.screen.blit(self.text_key, (W * 0.94, H * 0.19))
        self.screen.blit(self.text_gem, (W * 0.94, H * 0.24))
        self.screen.blit(self.text_coin, (W * 0.94, H * 0.29))

        #We also can do a for loop for this
        perm_objects = Inventory.perm_objects
        if perm_objects['Shovel'] == True:
            self.screen.blit(self.permanents_scaled['Shovel'], (W * 0.58, H * 0.43))
        if perm_objects['Lockpick_Kit'] == True:
            self.screen.blit(self.permanents_scaled['Lockpick_Kit'], (W * 0.68, H * 0.43))
        if perm_objects["Lucky_Rabbits_Foot"] == True:
            self.screen.blit(self.permanents_scaled["Lucky_Rabbits_Foot"], (W * 0.78, H * 0.43))
        if perm_objects['Metal_Detector'] == True:
            self.screen.blit(self.permanents_scaled['Metal_Detector'], (W * 0.86, H * 0.43))
        if perm_objects['Power_Hammer'] == True:
            self.screen.blit(self.permanents_scaled['Power_Hammer'], (W * 0.48, H * 0.53))

    def build_rooms(self):
        W, H = self.W, self.H
        room_size = (W // 18.5, W // 18.5)
        for name, img in self.room_images.items():
            self.rooms_scaled[name] = pygame.transform.scale(img, room_size)

    def blit_rooms(self):
        W, H = self.W, self.H
        step_y = H * 0.0959
        step_x = W * 0.054
        base_x = W * 0.2234
        base_y = H * 0.837

        for name, positions in Map.rooms.items():
            for row, col in positions:
                x = base_x + (col - 1) * step_x
                y = base_y - row * step_y  
                self.screen.blit(self.rooms_scaled[name], (x, y))

    # #Room : entrance hall
    # self.screen.blit(self.entranceHall, (W * 0.1695, H * 0.837))
