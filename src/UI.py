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
        pygame.display.set_caption("Blue prince 2D") #window name

        screen = pygame.display.set_mode(self.resolution)

        #back ground image
        path_bg_image = "../images/back_ground/bg_image.png"
        bg_image = pygame.image.load(path_bg_image)
        bg_image = pygame.transform.scale(bg_image,self.resolution)
        screen.blit(bg_image, (0,0))

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
    
    def update_item(self):
        W, H = self.resolution
        
        text_step = self.font.render(str(self.consumable["step"]), True, (255, 255, 255))
        text_key = self.font.render(str(self.consumable["key"]), True, (255, 255, 255))
        text_gem = self.font.render(str(self.consumable["gem"]), True, (255, 255, 255))
        text_coin = self.font.render(str(self.consumable["coin"]), True, (255, 255, 255))
        self.screen.blit(text_step, (W * 0.94, H * 0.14))
        self.screen.blit(text_key, (W * 0.94, H * 0.19))
        self.screen.blit(text_gem, (W * 0.94, H * 0.24))
        self.screen.blit(text_coin, (W * 0.94, H * 0.29))



        