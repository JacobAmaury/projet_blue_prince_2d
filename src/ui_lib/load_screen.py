import pygame
import database

from .image import Image, ImageSimple
from .window import Screen

class LoadScreen(Screen) :
    #convention : image = instance of Image, img = Surface

    def __init__(self):
        Screen.__init__(self)
        #load images
        bg_path="../images/background/BluePrince_Start.jpg"
        logo_path="../images/Logo_Blue_Prince.png"
        Screen.bg_image = ImageSimple(Image.loadFull(bg_path))
        self.logo_image = ImageSimple(Image.loadTransparent(logo_path))
        #show window (was Hidden)
        self.window.show_window()
        self.update()


    def update(self):
        buffer = self.window.buffer
        ##build_load_screen
        W,H = self.window.size
        self.size = W,H
        #images
        Screen.bg_image.smoothscale((W,H))
        Screen.bg_image.position = (0,0)
        self.logo_image.smoothscale((W//3, H//3))
        self.logo_image.position = (W//3 - self.logo_image.scaled.get_width()//2, H//20)

        ##blit_load_screen
        #images
        self.bg_image.blit(buffer)
        self.logo_image.blit(buffer)   
        #text (build and blit)
        self.print("Loading game ...")
        
        ##flip
        pygame.display.flip()



    def load_images(self):
        #background image mainscreen
        path = "../images/background/bg_image.png"
        Screen.main_bg_img = Image.loadFull(path)
        #shop bg
        path = "../images/background/shop.jpg"
        Screen.shop = ImageSimple(Image.loadFull(path))
        #explore bg
        colors = ['violet']
        for color in colors:
            path = f"../images/background/{color}_room.jpeg"
            Screen.bg_color_images[color] = ImageSimple(Image.loadFull(path))
        colors = ['blue','orange', 'red', 'green']
        for color in colors:
            path = f"../images/background/{color}_room.jpg"
            Screen.bg_color_images[color] = ImageSimple(Image.loadFull(path))

        #consumables
        for name in database.consumables :
            path = "../images/items/consumables/"+ name +"_icon.png"
            Screen.consumable_imgs[name] = Image.loadTransparent(path)
        #permanent objects
        for name in database.permanents:
            path = "../images/items/permanents/"+ name +"_White_Icon.png"
            Screen.permanant_imgs[name] = Image.loadTransparent(path)
        #other objects
        for name in database.others:
            path = f"../images/items/others/{name}.png"
            Screen.other_imgs[name] = Image.loadTransparent(path)

        #rooms : import all rooms by names from Rooms_db.rooms
        event_listener = self.window.ui.event_listener
        for name,room_data in database.rooms.items():
            path = "../images/rooms/"+ room_data['color'] +'/'+ name +'.png'
            Screen.room_imgs[name] = Image.loadFull(path)
            event_listener() #room loading may be long : handles user input

        #image menu
        bg_menu_path = "../images/background/selection_menu.png"
        Screen.selectionmenu_bg_img = Image.loadTransparent(bg_menu_path)

        #door status
        path = "../images/items/doors/closed_door.png"
        Screen.closed_door_img = Image.loadTransparent(path)
        path = "../images/items/doors/opened_door.png"
        Screen.opened_door_img = Image.loadTransparent(path)