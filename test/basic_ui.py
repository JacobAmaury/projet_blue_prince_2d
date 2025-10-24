import __src_path   #set path ../src

import pygame
from navigation import Nav      # pyright: ignore[reportMissingImports]

class UI :
    @classmethod
    def __init__(cls):
        pygame.display.set_mode(flags=pygame.HIDDEN)
        print('Loading game ...')
        print('! Click on terminal to refocus !')
        cls.nav = Nav(cls)    #initialise Navigation (=game controller)
        cls.nav.new_game()     #start a new game

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


