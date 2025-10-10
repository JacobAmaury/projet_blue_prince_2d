import pygame

#self.permanant_object = {'shovel':False, 'lockpick_kit':False, 'lucky_rabbit_foot':False, 'metal_detector':False, 'hammer':False} 
#self.consumable = {'step':50, 'coin':0, 'gem':0, 'key':0, 'dice':0 }
class User_interface:
    def __init__(self, resolution, consumable, permanant_object):
        self.resolution = resolution #tuple (width, height)
        self.permanant_object = permanant_object
        self.consumable = consumable
        self.running = True             #if True the while loop in the main is running 
    
    def initial_screen(self):
        pygame.display.set_caption("Blue prince 2D") #window name

        screen = pygame.display.set_mode(self.resolution)
        pygame.display.flip()

        #back ground image
        path_bg_image = "../images/back_ground/bg_image.jpg"
        bg_image = pygame.image.load(path_bg_image)
        bg_image = pygame.transform.scale(bg_image,self.resolution)
        screen.blit(bg_image, (0,0))

        #initial image for consumable

