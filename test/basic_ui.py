import __src_path   #set path ../src
""" This is a terminal based UserInterface.
    It is meant to be changed based on Navigation's needs, and used as a reference for the actual ui.
"""


import pygame

class UI :
    def __init__(self,nav):
        pygame.display.set_mode(flags=pygame.HIDDEN)
        print('Loading game ...')
        UI.nav = nav

    @classmethod
    def mainScreen(cls):
        print("Change screen : MainScreen (enter 'x' to exit game)")
        cls.update_consumables()
        cls.update_permanents()
        cls.update_map()
        cls.update_door()

    @classmethod
    def update_consumables(cls):
        print('consumables : ')
        for name,value in cls.nav.inventory.consumables.items():
            print(f'    {name} : {value}')

    @classmethod
    def update_permanents(cls):
        print('permanents : ')
        for name in cls.nav.inventory.permanents:
            print(f'    {name}')

    @classmethod
    def update_map(cls):
        print('rooms : ')
        for name,values in cls.nav.map.rooms.items():
            print(f'    {name} : {values}')

    @classmethod
    def update_door(cls):
        y,x,r = cls.nav.map.door
        print(f'player position : layer = {y}, x = {x}, rot = {r}')

    @classmethod
    def selectionScreen_temp(cls,prompt_msg,items):
        #this function needs to be better defined
        print('Selection choice :')
        print(prompt_msg)
        for nb,i in enumerate(items):
            print(f'    {nb}. ',i)
        return int(input())
    
    @classmethod
    def event_listener(cls):
        value = input()
        if value == 'x':
            event_handler.escape()
        elif value == '':
            event_handler.enter()
        elif value == pygame.K_BACKSPACE:
            event_handler.back()
        elif value == 'z' or value == 'w' :
            event_handler.up()
        elif value == 's':
            event_handler.down()
        elif value == 'q' or value == 'a':
            event_handler.left()
        elif value == 'd':
            event_handler.right()

    @classmethod
    def quit_game(cls):
        pygame.quit()
        print('Game exited properly.')
        raise SystemExit() #or sys.exit()

## event_handlers for player inputs
# keyboard inputs
class event_handler :
    escape = UI.quit_game
    enter = lambda: print('enter')
    back = lambda: print('back')
    up = lambda: print('up')
    down = lambda: print('down')
    left = lambda: print('left')
    right = lambda: print('right')
UI.event_handler = event_handler


