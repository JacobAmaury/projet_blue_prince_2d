import database

class Inventory:
    def __init__(self,ui):
        Inventory.ui = ui
        Inventory.consumables = {'steps': 70, 'coin': 0, 'gem': 2, 'key': 0, 'dice': 0}
        Inventory.permanents = set()


    def change_consumable(self,name,increment):
        Inventory.consumables[name] += increment
        Inventory.ui.update_consumables()
    
    def change_perm(self,name,isinside):
        if name not in database.permanents :
            raise ValueError('name not in database')
        if isinside:
            Inventory.permanents.add(name)
        else :
            Inventory.permanents.remove(name)
        Inventory.ui.update_permanents()
