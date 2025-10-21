import pygame
import os

from options import Options
from data.rooms_db import Rooms_db


class Display:
    window_ratio = (16,9)
    room_images = {}    #loaded room images
    rooms = {}   #scaled room images

    def __init__(self):
        #import display_size
        self.desk_W, self.desk_H = pygame.display.get_desktop_sizes()[0]
        #set window_size based on default_window_size
        self.screen_set_size(Options.default_window_size)
        #text size
        self.font = pygame.font.Font(None, self.H // 25) 
        #load ressources
        self.load_ini_images()

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
        blueprince_icon = pygame.image.load(os.path.join("images", "blueprince_icon.jpeg"))
        pygame.display.set_icon(blueprince_icon)
        self.screen = pygame.display.set_mode((self.W, self.H),pygame.RESIZABLE)

    def load_ini_images(self):
        #load_screen
        path = os.path.join("images","background", "BluePrince_Start.jpg")
        self.bg_image_load = pygame.image.load(path)
        #Logo
        path = os.path.join("images", "Logo_Blue_Prince.png")
        self.image_logo = pygame.image.load(path)

    def build_load_screen(self):
        W,H = self.W,self.H
        #load_screen
        self.bg_load = pygame.transform.scale(self.bg_image_load,(W, H))
        self.bg_load_position = (0,H//2 - self.bg_load.get_height()//2)  #centre en H
        #Logo
        self.logo = pygame.transform.scale(self.image_logo,(W//3, H//3))
        self.logo_position = (W//3 - self.logo.get_height()//2,H//20,)
        #text
        self.loading_text = self.font.render("Loading game ...", True, (255, 255, 255))
        self.text_position = (W //2 - self.loading_text.get_width()//2, H * 0.95)


    def blit_load_screen(self):
        #create load_screen
        self.screen.blit(self.bg_load, self.bg_load_position)   
        #Logo
        self.screen.blit(self.logo,self.logo_position )    
        #text
        self.screen.blit(self.loading_text, self.text_position)

    def load_images(self,Rooms):
        #background image
        path = os.path.join("images","background", "bg_image.png")
        self.bg_image = pygame.image.load(path)
        
        #consumables
        path = os.path.join("images","items","consumables", "Gem_icon.png")
        self.gem_image = pygame.image.load(path)
        path = os.path.join("images","items","consumables", "Gold_Coin_icon.png")
        self.coin_image = pygame.image.load(path)
        path = os.path.join("images","items","consumables", "Ivory_Dice_icon.png")
        self.dice_image = pygame.image.load(path)
        path = os.path.join("images","items","consumables", "Key_icon.png")
        self.key_image = pygame.image.load(path)
        path = os.path.join("images","items","consumables", "Steps_icon.png")
        self.steps_image = pygame.image.load(path)

        #perm objects
        path = os.path.join("images","items","permanant_objects", "Shovel_White_Icon.png")
        self.shovel_image = pygame.image.load(path)
        path = os.path.join("images","items","permanant_objects",'Lockpick_White_Icon.png')
        self.lockpick_kit_image = pygame.image.load(path)
        path = os.path.join("images","items","permanant_objects",'Lucky_Rabbits_Foot_White_Icon.png')
        self.lucky_rabbit_foot_image = pygame.image.load(path)
        path = os.path.join("images","items","permanant_objects",'Metal_Detector_White_Icon.png')
        self.metal_detector_image = pygame.image.load(path)
        path = os.path.join("images","items","permanant_objects",'Power_Hammer_White_Icon.png')
        self.hammer_image = pygame.image.load(path)


        #rooms : names in data/rooms_db
        for name in Rooms_db.blue_rooms:
            path = os.path.join("images","rooms","blue_room", name+'.png')
            self.room_images[name] = pygame.image.load(path)
        for name in Rooms_db.yellow_rooms:
            path = os.path.join("images","rooms","shop", name+'.png')
            self.room_images[name] = pygame.image.load(path)
        for name in Rooms_db.orange_rooms:
            path = os.path.join("images","rooms","hallway", name+'.png')
            self.room_images[name] = pygame.image.load(path)
        for name in Rooms_db.violet_rooms:
            path = os.path.join("images","rooms","bedroom", name+'.png')
            self.room_images[name] = pygame.image.load(path)
        for name in Rooms_db.green_rooms:
            path = os.path.join("images","rooms","green_room", name+'.png')
            self.room_images[name] = pygame.image.load(path)
        for name in Rooms_db.red_rooms:
            path = os.path.join("images","rooms","red_room", name+'.png')
            self.room_images[name] = pygame.image.load(path)

    def build_bg_screen(self):
        W, H = self.W,self.H
        #back ground image
        self.bg = pygame.transform.scale(self.bg_image,(W, H))
        #size for consumable_images
        consumable_size = (H//20,H//20)
        self.gem = pygame.transform.scale(self.gem_image,consumable_size)
        self.coin = pygame.transform.scale(self.coin_image,consumable_size)
        self.dice = pygame.transform.scale(self.dice_image,consumable_size)
        self.key = pygame.transform.scale(self.key_image,consumable_size)
        self.steps = pygame.transform.scale(self.steps_image,consumable_size)
        

    def blit_bg_screen(self):
        W, H = self.W,self.H
        #back ground image
        self.screen.blit(self.bg, (0,0))
        
        #responsive position
        self.screen.blit(self.steps, (W * 0.91, H * 0.13))
        self.screen.blit(self.key,   (W * 0.91, H * 0.18))
        self.screen.blit(self.gem,   (W * 0.91, H * 0.23))  
        self.screen.blit(self.coin,  (W * 0.91, H * 0.28)) 
        # screen.blit(self.dice,  (W * 0.91, H * 0.)) #I don't kwon were it go
    
    def build_items(self,consumables):
        W, H = self.W,self.H
        perm_size = (W//11, H//11)
        #consumable cpt 
        self.text_step = self.font.render(str(consumables["step"]), True, (255, 255, 255))
        self.text_key = self.font.render(str(consumables["key"]), True, (255, 255, 255))
        self.text_gem = self.font.render(str(consumables["gem"]), True, (255, 255, 255))
        self.text_coin = self.font.render(str(consumables["coin"]), True, (255, 255, 255))
    
        #permanent objects
        self.shovel = pygame.transform.scale(self.shovel_image, perm_size)
        self.lockpick_kit = pygame.transform.scale(self.lockpick_kit_image, perm_size)
        self.lucky_rabbit_foot = pygame.transform.scale(self.lucky_rabbit_foot_image, perm_size)
        self.metal_detector = pygame.transform.scale(self.metal_detector_image, perm_size)
        self.hammer = pygame.transform.scale(self.hammer_image, perm_size)

    def blit_items(self,permanant_objects):
        W, H = self.W,self.H
        #consumable cpt 
        self.screen.blit(self.text_step, (W * 0.94, H * 0.14))
        self.screen.blit(self.text_key, (W * 0.94, H * 0.19))
        self.screen.blit(self.text_gem, (W * 0.94, H * 0.24))
        self.screen.blit(self.text_coin, (W * 0.94, H * 0.29))

        #We also can do a for loop for this
        if permanant_objects['shovel'] == True:
            self.screen.blit(self.shovel, (W * 0.58, H * 0.43))
        
        if permanant_objects['lockpick_kit'] == True:
            self.screen.blit(self.lockpick_kit, (W * 0.68, H * 0.43))
        
        if permanant_objects['lucky_rabbit_foot'] == True:
            self.screen.blit(self.lucky_rabbit_foot, (W * 0.78, H * 0.43))
        
        if permanant_objects['metal_detector'] == True:
            self.screen.blit(self.metal_detector, (W * 0.86, H * 0.43))
        
        if permanant_objects['hammer'] == True:
            self.screen.blit(self.hammer, (W * 0.48, H * 0.53))

    def build_rooms(self,Rooms):
        W, H = self.W, self.H
        room_size = (W // 18.5, W // 18.5)
        for name, _ in Rooms.rooms.items():
            self.rooms[name] = pygame.transform.scale(self.room_images[name], room_size)

    def blit_rooms(self, Rooms):
        W, H = self.W, self.H
        step_y = H * 0.0959
        step_x = W * 0.054
        base_x = W * 0.2234
        base_y = H * 0.837

        for name, positions in Rooms.rooms.items():
            for row, col in positions:
                x = base_x + (col - 1) * step_x
                y = base_y - row * step_y  
                self.screen.blit(self.rooms[name], (x, y))

    # #Room : entrance hall
    # self.screen.blit(self.entranceHall, (W * 0.1695, H * 0.837))
