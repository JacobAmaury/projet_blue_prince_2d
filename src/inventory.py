import database

class Inventory:
    def __init__(self,ui):
        Inventory.ui = ui
        Inventory.consumables = {'steps': 70, 'coin': 0, 'gem': 2, 'key': 0, 'dice': 0}
        Inventory.permanents = set()


    @classmethod
    def change_consumable(cls,name,increment):
        cls.consumables[name] += increment
        cls.ui.update_consumables()

    @classmethod
    def change_perm(cls,name,isinside):
        if name not in database.permanents :
            raise ValueError('name not in database')
        if isinside:
            cls.permanents.add(name)
        else :
            cls.permanents.remove(name)
        cls.ui.update_permanents()
