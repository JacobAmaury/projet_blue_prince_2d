from ui import UI


class Inventory:
    consumables = {'step': 50, 'coin': 3, 'gem': 2, 'key': 1, 'dice': 0}
    permanant_objects = {'shovel': True, 'lockpick_kit': False, 'lucky_rabbit_foot': True, 'metal_detector': False, 'hammer': True}


    def change_consumable(name,increment):
        Inventory.consumables[name] += increment
        UI.instance.update_consumables()
    
    def change_permanents(name,value):
        Inventory.permanant_objects[name] = value
        UI.instance.update_permanents()