import pygame
import os

from Options import Options
from Dev import Dev

class UI:
    window_ratio = (16,9)

    def __init__(self,window_size = Options.window_size, consumables= Dev.initial_consumables, permanant_objects=Dev.initial_permanant_objects):
        
        self.permanant_objects = permanant_objects
        self.consumables= consumables

        #ini pygame
        pygame.init() #(nb loaded modules, nb failed)

        #window attributes
        (desk_w,desk_h) = pygame.display.get_desktop_sizes()[0]
        (width,height) = window_size
        #if display < window_size
        while width > desk_w or height > desk_h :
            width -= self.window_ratio[0] ; height -= self.window_ratio[1]
        self.win_size = (width,height)
        Options.window_size = (width,height)    #problème d'organisation

        #window creation
        pygame.display.set_caption("Blue prince 2D")
        blueprince_icon = pygame.image.load(os.path.join("images", "blueprince_icon.jpeg"))
        pygame.display.set_icon(blueprince_icon)
        self.screen = pygame.display.set_mode(self.win_size)
        
        #text
        #pygame.font.init() 
        self.font = pygame.font.Font(None, height // 25) 

    def initial_screen(self):

        #back ground image
        path_bg_image = os.path.join("images","background", "bg_image.png")
        bg_image = pygame.image.load(path_bg_image)
        bg_image = pygame.transform.scale(bg_image,self.win_size)
        self.screen.blit(bg_image, (0,0))

        #size for consumable_images
        consumable_size = tuple([self.win_size[1]//20]*2)
        
        #I think we could use a loop to do this
        path_gem = os.path.join("images","items","consumables", "Gem_icon.png")
        path_coin = os.path.join("images","items","consumables", "Gold_Coin_icon.png")
        path_dice = os.path.join("images","items","consumables", "Ivory_Dice_icon.png")
        path_key = os.path.join("images","items","consumables", "Key_icon.png")
        path_steps = os.path.join("images","items","consumables", "Steps_icon.png")
        
        gem_image = pygame.image.load(path_gem)
        coin_image = pygame.image.load(path_coin)
        dice_image = pygame.image.load(path_dice)
        key_image = pygame.image.load(path_key)
        steps_image = pygame.image.load(path_steps)

        gem_image = pygame.transform.scale(gem_image,consumable_size)
        coin_image = pygame.transform.scale(coin_image,consumable_size)
        dice_image = pygame.transform.scale(dice_image,consumable_size)
        key_image = pygame.transform.scale(key_image,consumable_size)
        steps_image = pygame.transform.scale(steps_image,consumable_size)
        
        #responsive position
        W, H = self.win_size
        self.screen.blit(steps_image, (W * 0.91, H * 0.13))
        self.screen.blit(key_image,   (W * 0.91, H * 0.18))
        self.screen.blit(gem_image,   (W * 0.91, H * 0.23))  
        self.screen.blit(coin_image,  (W * 0.91, H * 0.28)) 
        # screen.blit(dice_image,  (W * 0.91, H * 0.)) #I don't kwon were it go

        #Room : entrance hall
        room_size = W//18.5, W//18.5
        path_room = os.path.join("images","rooms","blue_room", "EntranceHall.png")
        room_image = pygame.image.load(path_room)
        room_image = pygame.transform.scale(room_image, room_size)
        self.screen.blit(room_image, (W * 0.1695, H * 0.837))


    def update_item(self):
        self.initial_screen()
        
        W, H = self.win_size
        perm_size = (W//11, H//11)
        #consumable cpt 
        text_step = self.font.render(str(self.consumables["step"]), True, (255, 255, 255))
        text_key = self.font.render(str(self.consumables["key"]), True, (255, 255, 255))
        text_gem = self.font.render(str(self.consumables["gem"]), True, (255, 255, 255))
        text_coin = self.font.render(str(self.consumables["coin"]), True, (255, 255, 255))
        self.screen.blit(text_step, (W * 0.94, H * 0.14))
        self.screen.blit(text_key, (W * 0.94, H * 0.19))
        self.screen.blit(text_gem, (W * 0.94, H * 0.24))
        self.screen.blit(text_coin, (W * 0.94, H * 0.29))

        #We also can do a for loop for this
        if self.permanant_objects['shovel'] == True:
            path_shovel = os.path.join("images","items","permanant_objects", "Shovel_White_Icon.png")
            shovel_image = pygame.image.load(path_shovel)
            shovel_image = pygame.transform.scale(shovel_image, perm_size)
            self.screen.blit(shovel_image, (W * 0.58, H * 0.43))
        
        if self.permanant_objects['lockpick_kit'] == True:
            path_lockpick_kit = os.path.join("images","items","permanant_objects",'Lockpick_White_Icon.png')
            lockpick_kit_image = pygame.image.load(path_lockpick_kit)
            lockpick_kit_image = pygame.transform.scale(lockpick_kit_image, perm_size)
            self.screen.blit(lockpick_kit_image, (W * 0.68, H * 0.43))
        
        if self.permanant_objects['lucky_rabbit_foot'] == True:
            path_lucky_rabbit_foot = os.path.join("images","items","permanant_objects",'Lucky_Rabbits_Foot_White_Icon.png')
            lucky_rabbit_foot_image = pygame.image.load(path_lucky_rabbit_foot)
            lucky_rabbit_foot_image = pygame.transform.scale(lucky_rabbit_foot_image, perm_size)
            self.screen.blit(lucky_rabbit_foot_image, (W * 0.78, H * 0.43))
        
        if self.permanant_objects['metal_detector'] == True:
            path_metal_detector = os.path.join("images","items","permanant_objects",'Metal_Detector_White_Icon.png')
            metal_detector_image = pygame.image.load(path_metal_detector)
            metal_detector_image = pygame.transform.scale(metal_detector_image, perm_size)
            self.screen.blit(metal_detector_image, (W * 0.86, H * 0.43))
        
        if self.permanant_objects['hammer'] == True:
            path_hammer = os.path.join("images","items","permanant_objects",'Power_Hammer_White_Icon.png')
            hammer_image = pygame.image.load(path_hammer)
            hammer_image = pygame.transform.scale(hammer_image, perm_size)
            self.screen.blit(hammer_image, (W * 0.48, H * 0.53))

    def place_room_map(self, rooms):
        W, H = self.win_size
        room_size = (W // 18.5, W // 18.5)
        step_y = H * 0.0959
        step_x = W * 0.054
        base_x = W * 0.2234
        base_y = H * 0.837

        for name, positions in rooms.items():
            for row, col in positions:
                path_room = os.path.join("images","rooms","blue_room", name+'.png')
                room_image = pygame.image.load(path_room)
                room_image = pygame.transform.scale(room_image, room_size)

                x = base_x + (col - 1) * step_x
                y = base_y - row * step_y  
                self.screen.blit(room_image, (x, y))