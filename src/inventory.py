

class Inventory:
    def __init__(self,ui):
        Inventory.ui = ui
        Inventory.consumables = {'steps': 70, 'coin': 0, 'gem': 2, 'key': 0, 'dice': 0}
        Inventory.perm_objects = {
        'Shovel': False, 
        'Lockpick_Kit': False, 
        'Lucky_Rabbits_Foot': False, 
        'Metal_Detector': False, 
        'Power_Hammer': False
        }


    def change_consumable(self,name,increment):
        Inventory.consumables[name] += increment
        Inventory.ui.update_consumables()
    
    def change_perm(self,name,value):
        Inventory.perm_objects[name] = value
        Inventory.ui.update_permanents()
