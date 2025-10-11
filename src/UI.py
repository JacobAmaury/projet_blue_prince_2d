import pygame

#self.permanant_object = {'shovel':False, 'lockpick_kit':False, 'lucky_rabbit_foot':False, 'metal_detector':False, 'hammer':False} 
#self.consumable = {'step':50, 'coin':0, 'gem':0, 'key':0, 'dice':0 }

class User_interface:
    def __init__(self, resolution, consumable, permanant_object):
        self.resolution = resolution #tuple (width, height)
        self.permanant_object = permanant_object
        self.consumable = consumable
        self.running = True             #if True the while loop in the main is running 
        
        pygame.display.set_caption("Blue prince 2D") #window name
        self.screen = pygame.display.set_mode(resolution)
        
        #for display text
        pygame.font.init() 
        self.font = pygame.font.Font(None, resolution[1] // 25) 

    
    def initial_screen(self):

        #back ground image
        path_bg_image = "../images/back_ground/bg_image.png"
        bg_image = pygame.image.load(path_bg_image)
        bg_image = pygame.transform.scale(bg_image,self.resolution)
        self.screen.blit(bg_image, (0,0))

        #initial image for consumable
        consumable_resolution = self.resolution[1]//20
        consumable_resolution = (consumable_resolution, consumable_resolution) 
        
        #I think we could use a loop to do this
        path_gem = "../images/items/consumable/Gem_icon.png"
        path_coin = "../images/items/consumable/Gold_Coin_icon.png"
        path_dice = "../images/items/consumable/Ivory_Dice_icon.png"
        path_key = "../images/items/consumable/Key_icon.png"
        path_steps = "../images/items/consumable/Steps_icon.png"
        
        gem_image = pygame.image.load(path_gem)
        coin_image = pygame.image.load(path_coin)
        dice_image = pygame.image.load(path_dice)
        key_image = pygame.image.load(path_key)
        steps_image = pygame.image.load(path_steps)

        gem_image = pygame.transform.scale(gem_image,consumable_resolution)
        coin_image = pygame.transform.scale(coin_image,consumable_resolution)
        dice_image = pygame.transform.scale(dice_image,consumable_resolution)
        key_image = pygame.transform.scale(key_image,consumable_resolution)
        steps_image = pygame.transform.scale(steps_image,consumable_resolution)
        
        #responsive position
        W, H = self.resolution
        self.screen.blit(steps_image, (W * 0.91, H * 0.13))
        self.screen.blit(key_image,   (W * 0.91, H * 0.18))
        self.screen.blit(gem_image,   (W * 0.91, H * 0.23))  
        self.screen.blit(coin_image,  (W * 0.91, H * 0.28)) 
        # screen.blit(dice_image,  (W * 0.91, H * 0.)) #I don't kwon were it go

        room_resolution = W//18.5, W//18.5
        path_room = '../images/room/blue_room/EntranceHall.png'
        room_image = pygame.image.load(path_room)
        room_image = pygame.transform.scale(room_image, room_resolution)
        self.screen.blit(room_image, (W * 0.1695, H * 0.837))



    def update_item(self):
        self.initial_screen()
        
        W, H = self.resolution
        perm_reso = (self.resolution[0]//11, self.resolution[1]//11)
        #consumable cpt 
        text_step = self.font.render(str(self.consumable["step"]), True, (255, 255, 255))
        text_key = self.font.render(str(self.consumable["key"]), True, (255, 255, 255))
        text_gem = self.font.render(str(self.consumable["gem"]), True, (255, 255, 255))
        text_coin = self.font.render(str(self.consumable["coin"]), True, (255, 255, 255))
        self.screen.blit(text_step, (W * 0.94, H * 0.14))
        self.screen.blit(text_key, (W * 0.94, H * 0.19))
        self.screen.blit(text_gem, (W * 0.94, H * 0.24))
        self.screen.blit(text_coin, (W * 0.94, H * 0.29))

        #We also can do a for loop for this
        if self.permanant_object['shovel'] == True:
            path_shovel = '../images/items/permanant_object/Shovel_White_Icon.png'
            shovel_image = pygame.image.load(path_shovel)
            shovel_image = pygame.transform.scale(shovel_image, perm_reso)
            self.screen.blit(shovel_image, (W * 0.58, H * 0.43))
        
        if self.permanant_object['lockpick_kit'] == True:
            path_lockpick_kit = '../images/items/permanant_object/Lockpick_White_Icon.png'
            lockpick_kit_image = pygame.image.load(path_lockpick_kit)
            lockpick_kit_image = pygame.transform.scale(lockpick_kit_image, perm_reso)
            self.screen.blit(lockpick_kit_image, (W * 0.68, H * 0.43))
        
        if self.permanant_object['lucky_rabbit_foot'] == True:
            path_lucky_rabbit_foot = '../images/items/permanant_object/Lucky_Rabbits_Foot_White_Icon.png'
            lucky_rabbit_foot_image = pygame.image.load(path_lucky_rabbit_foot)
            lucky_rabbit_foot_image = pygame.transform.scale(lucky_rabbit_foot_image, perm_reso)
            self.screen.blit(lucky_rabbit_foot_image, (W * 0.78, H * 0.43))
        
        if self.permanant_object['metal_detector'] == True:
            path_metal_detector = '../images/items/permanant_object/Metal_Detector_White_Icon.png'
            metal_detector_image = pygame.image.load(path_metal_detector)
            metal_detector_image = pygame.transform.scale(metal_detector_image, perm_reso)
            self.screen.blit(metal_detector_image, (W * 0.86, H * 0.43))
        
        if self.permanant_object['hammer'] == True:
            path_hammer = '../images/items/permanant_object/Power_Hammer_White_Icon.png'
            hammer_image = pygame.image.load(path_hammer)
            hammer_image = pygame.transform.scale(hammer_image, perm_reso)
            self.screen.blit(hammer_image, (W * 0.48, H * 0.53))

    def place_room_map(self, rooms):
            W, H = self.resolution 
            room_resolution = (W // 18.5, W // 18.5)
            step_y = H * 0.0959
            step_x = W * 0.054
            base_x = W * 0.2234
            base_y = H * 0.837

            for name, positions in rooms.items():
                for row, col in positions:
                    path_room = f'../images/room/blue_room/{name}.png'
                    room_image = pygame.image.load(path_room)
                    room_image = pygame.transform.scale(room_image, room_resolution)

                    x = base_x + (col - 1) * step_x
                    y = base_y - row * step_y  
                    self.screen.blit(room_image, (x, y))