import pygame

from options import Options
from rooms_db import Rooms_db
from inventory import Inventory
from map import Map

from .load_screen import loadScreen
from .inventory_grid import Permanent,Consumable
from .map_grid import Room,map

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
        _,H = self.size
        self.font = pygame.font.Font(None, H // 25) 
        #load load_screen images
        self.loadScreen = loadScreen(bg_path="../images/background/BluePrince_Start.jpg",
                             logo_path="../images/Logo_Blue_Prince.png")

    def screen_set_size(self,window_size):
        W,H = window_size
        self.size = W,H
        #if default_window_size > display_size
        if W > self.desk_W or H > self.desk_H :
            self.maximize_window_v1(self.desk_W,self.desk_H)
        #set window_size
        Options.window_size = self.size

    def maximize_window_v1(self,desk_w,desk_h):
        #maximize window to biggest size inferior to current, keeping window_ratio
        W,H = self.size
        while W > desk_w or H > desk_h :
            W -= self.window_ratio[0] ; H -= self.window_ratio[1]
        self.size = (W,H)

    def create_window(self):
        #window creation
        pygame.display.set_caption("Blue prince 2D")
        blueprince_icon = pygame.image.load("../images/blueprince_icon.jpeg")
        pygame.display.set_icon(blueprince_icon)
        self.screen = pygame.display.set_mode(self.size,pygame.RESIZABLE)

    def build_and_blit_loadScreen(self):
        W,H = self.size
        self.loadScreen.build_and_blit(W,H,self.font,self.screen)

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
        W, H = self.size
        #back ground image
        self.bg = pygame.transform.smoothscale(self.bg_image,(W, H))

        #build consumable images
        #size for consumable_images
        consumable_size = (H//20,H//20) #square
        for imageC in self.consumable_images:
            imageC.scaled = pygame.transform.scale(imageC.loaded,consumable_size)

    def blit_bg_screen(self):
        W, H = self.size
        #back ground image
        self.screen.blit(self.bg, (0,0))
        
        #consumables :responsive position
        for id,consumable in enumerate(self.consumable_images):
            self.screen.blit(consumable.scaled, Consumable.get_position_img(id))    #issue with dice position
    
    def build_items(self):
        #consumable cpt 
        inventory_consumables = Inventory.consumables
        for consumable in self.consumable_images:
            consumable.txt = self.font.render(str(inventory_consumables[consumable.name]), True, (255, 255, 255))

        #permanent objects
        W, H = self.size
        perm_size = (W//11, H//11)
        for permanent in self.permanent_images :
            permanent.scaled = pygame.transform.scale(permanent.loaded,perm_size)

    def blit_items(self):
        W, H = self.size
        #consumable cpt 
        for id,consumable in enumerate(self.consumable_images):
            self.screen.blit(consumable.txt, Consumable.get_position_txt(id))

        #permanents
        inv_permanents = Inventory.perm_objects
        for id,permanent in enumerate(self.permanent_images):
            if inv_permanents[permanent.name] == True:
                self.screen.blit(permanent.scaled, Permanent.get_position_img(id))

    def build_rooms(self):
        W, H = self.size
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
        W, H = self.size
        for name, position in Map.rooms.items():
            room_image = self.room_images[name]
            for row, col, angle in position:
                self.screen.blit(room_image.rot[angle], room_image.get_position_case(col,row))

    def set_all_grids_mainScreen(self):
        """recalculates x,y,step_x,step_y of all grids of mainScreen"""
        W, H = self.size
        map.set_grid(W,H)
        Consumable.set_grid(W,H)
        Permanent.set_grid(W,H)