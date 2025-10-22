

class Inventory:
    def __init__(self,ui):
        Inventory.ui = ui

    consumables = {'steps': 50, 'coin': 3, 'gem': 2, 'key': 1, 'dice': 0}
    perm_objects = {
        'Shovel': True, 
        'Lockpick_Kit': False, 
        'Lucky_Rabbits_Foot': True, 
        'Metal_Detector': False, 
        'Power_Hammer': True
        }


    def change_consumable(self,name,increment):
        Inventory.consumables[name] += increment
        Inventory.ui.update_consumables()
    
    def change_perm(self,name,value):
        Inventory.perm_objects[name] = value
        Inventory.ui.update_permanents()