

class Inventory:
    def __init__(self,ui):
        self.ui = ui

    consumables = {'step': 50, 'coin': 3, 'gem': 2, 'key': 1, 'dice': 0}
    permanant_objects = {'shovel': True, 'lockpick_kit': False, 'lucky_rabbit_foot': True, 'metal_detector': False, 'hammer': True}


    def change_consumable(self,name,increment):
        Inventory.consumables[name] += increment
        self.ui.update_consumables()
    
    def change_permanents(self,name,value):
        Inventory.permanant_objects[name] = value
        self.ui.update_permanents()