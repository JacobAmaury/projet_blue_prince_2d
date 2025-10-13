

class Dev :
    initial_consumables = {'step': 50, 'coin': 3, 'gem': 2, 'key': 1, 'dice': 0}
    initial_permanant_objects = {'shovel': True, 'lockpick_kit': True, 'lucky_rabbit_foot': True, 'metal_detector': True, 'hammer': True}
    rooms = {
        "Mechanarium": [(1, 0),(2,-2)],
        "MusicRoom": [(2, 0)],
        "Security": [(2, -1)]
    }
    #self.permanant_object = {'shovel':False, 'lockpick_kit':False, 'lucky_rabbit_foot':False, 'metal_detector':False, 'hammer':False} 
    #self.consumable = {'step':50, 'coin':0, 'gem':0, 'key':0, 'dice':0 }
