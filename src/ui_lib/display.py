import pygame

import database
from options import Options
from inventory import Inventory
from map import Map

from .load_screen import loadScreen
from .inventory_grid import Permanent,Consumable
from .map_grid import Room,map

class Display:
    WINDOW_RATIO = (16,9)

    permanent_images = []   #list : order on screen
    consumable_images = []
    room_images = {}        #dict : no preset order on screen

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
        ratio_W, ratio_H = self.WINDOW_RATIO
        W,H = self.size
        while W > desk_w or H > desk_h :
            W -= ratio_W ; H -= ratio_H
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
        #create variables
        for name in database.consumables:
            Display.consumable_images.append(Consumable(name))
        for name in database.permanents:
            Display.permanent_images.append(Permanent(name))

        #background image
        path = "../images/background/bg_image.png"
        self.bg_image = pygame.image.load(path).convert()

        #consumables
        for image in self.consumable_images :
            path = "../images/items/consumables/"+ image.name +"_icon.png"
            image.loaded = pygame.image.load(path).convert_alpha()

        #permanent objects
        for image in self.permanent_images :
            path = "../images/items/permanant_objects/"+ image.name +"_White_Icon.png"
            image.loaded = pygame.image.load(path).convert_alpha()

        #rooms : import all rooms by names from Rooms_db.rooms
        for name,color in database.rooms.items():
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
        for image in self.consumable_images:
            image.scaled = pygame.transform.scale(image.loaded,consumable_size)

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
        inv_permanents = Inventory.permanents
        for id,permanent in enumerate(self.permanent_images):
            if permanent.name in inv_permanents:
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