import pygame
import os

from options import Options
from inventory import Inventory
from rooms import Rooms

#Note : Transform and render should be done only on resize_event

class Window:
    window_ratio = (16,9)

    def __init__(self):
        #import display_size
        self.desk_W, self.desk_H = pygame.display.get_desktop_sizes()[0]
        #text initalisation
        #pygame.font.init()
        #set window to default window_size
        self.screen_set_size(Options._window_size)
        #load ressources
        self.load_ini_images()

    def screen_set_size(self,window_size):
        W,H = window_size
        self.W, self.H = W,H
        #if default_window_size > display_size
        if self.W > self.desk_W or self.H > self.desk_H :
            self.maximize_window_v1(self.desk_W,self.desk_H)
        #text size
        self.font = pygame.font.Font(None, self.H // 25) 
        #change default window_size if different
        if Options._window_size[0] != W or Options._window_size[0] != H :
            Options._window_size = (W,H)

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

    def blit_load_screen(self):
        W,H = self.W,self.H

        #create load_screen
        bg_image = pygame.transform.scale(self.bg_image_load,(W, H))
        self.screen.blit(bg_image, (0,H//2 - bg_image.get_height()//2))    #centre en H

        #Logo
        image = pygame.transform.scale(self.image_logo,(W//3, H//3))
        logo_position = (W//3 - image.get_height()//2,H//20,)
        self.screen.blit(image,logo_position )    

        #text
        loading_text = self.font.render("Loading game ...", True, (255, 255, 255))
        text_position = (W //2 - loading_text.get_width()//2, H * 0.95)
        self.screen.blit(loading_text, text_position)

        #display
        pygame.display.flip()

    def load_images(self):
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

        #rooms
        path = os.path.join("images","rooms","blue_room", "EntranceHall.png")
        self.entranceHall = pygame.image.load(path)

    def blit_main_screen(self):
        W, H = self.W,self.H
        #back ground image
        bg_image = pygame.transform.scale(self.bg_image,(W, H))
        self.screen.blit(bg_image, (0,0))

        #size for consumable_images
        consumable_size = (H//20,H//20)

        gem_image = pygame.transform.scale(self.gem_image,consumable_size)
        coin_image = pygame.transform.scale(self.coin_image,consumable_size)
        dice_image = pygame.transform.scale(self.dice_image,consumable_size)
        key_image = pygame.transform.scale(self.key_image,consumable_size)
        steps_image = pygame.transform.scale(self.steps_image,consumable_size)
        
        #responsive position
        self.screen.blit(steps_image, (W * 0.91, H * 0.13))
        self.screen.blit(key_image,   (W * 0.91, H * 0.18))
        self.screen.blit(gem_image,   (W * 0.91, H * 0.23))  
        self.screen.blit(coin_image,  (W * 0.91, H * 0.28)) 
        # screen.blit(dice_image,  (W * 0.91, H * 0.)) #I don't kwon were it go

        #Room : entrance hall
        room_size = W//18.5, W//18.5
        room_image = pygame.transform.scale(self.entranceHall, room_size)
        self.screen.blit(room_image, (W * 0.1695, H * 0.837))

    
    def blit_items(self,consumables,permanant_objects):
        W, H = self.W,self.H
        perm_size = (W//11, H//11)
        #consumable cpt 
        text_step = self.font.render(str(consumables["step"]), True, (255, 255, 255))
        text_key = self.font.render(str(consumables["key"]), True, (255, 255, 255))
        text_gem = self.font.render(str(consumables["gem"]), True, (255, 255, 255))
        text_coin = self.font.render(str(consumables["coin"]), True, (255, 255, 255))
        self.screen.blit(text_step, (W * 0.94, H * 0.14))
        self.screen.blit(text_key, (W * 0.94, H * 0.19))
        self.screen.blit(text_gem, (W * 0.94, H * 0.24))
        self.screen.blit(text_coin, (W * 0.94, H * 0.29))

        #We also can do a for loop for this
        if permanant_objects['shovel'] == True:
            shovel_image = pygame.transform.scale(self.shovel_image, perm_size)
            self.screen.blit(shovel_image, (W * 0.58, H * 0.43))
        
        if permanant_objects['lockpick_kit'] == True:
            lockpick_kit_image = pygame.transform.scale(self.lockpick_kit_image, perm_size)
            self.screen.blit(lockpick_kit_image, (W * 0.68, H * 0.43))
        
        if permanant_objects['lucky_rabbit_foot'] == True:
            lucky_rabbit_foot_image = pygame.transform.scale(self.lucky_rabbit_foot_image, perm_size)
            self.screen.blit(lucky_rabbit_foot_image, (W * 0.78, H * 0.43))
        
        if permanant_objects['metal_detector'] == True:
            metal_detector_image = pygame.transform.scale(self.metal_detector_image, perm_size)
            self.screen.blit(metal_detector_image, (W * 0.86, H * 0.43))
        
        if permanant_objects['hammer'] == True:
            hammer_image = pygame.transform.scale(self.hammer_image, perm_size)
            self.screen.blit(hammer_image, (W * 0.48, H * 0.53))

    def blit_rooms(self, rooms):
        W, H = self.W, self.H
        room_size = (W // 18.5, W // 18.5)
        step_y = H * 0.0959
        step_x = W * 0.054
        base_x = W * 0.2234
        base_y = H * 0.837

        for name, positions in rooms.items():
            for row, col in positions:
                path_room = os.path.join("images","rooms","blue_room", name+'.png') #should pre-load all
                room_image = pygame.image.load(path_room)
                room_image = pygame.transform.scale(room_image, room_size)

                x = base_x + (col - 1) * step_x
                y = base_y - row * step_y  
                self.screen.blit(room_image, (x, y))

    def blit_bg_items_rooms(self):
        self.blit_main_screen()
        self.blit_items(Inventory.consumables, Inventory.permanant_objects) 
        self.blit_rooms(Rooms.rooms)
