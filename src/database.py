#names used for images loading in Display

consumables = ['steps', 'coin', 'gem', 'key', 'dice'] #sets the order on screen
permanents = ['Shovel','Lockpick_Kit','Lucky_Rabbits_Foot','Metal_Detector','Power_Hammer']

#|-2--|
#3    1          doors = [0,1,2,3]
#|_0__|

#rarity : 0 common, 1 standar, 2 unusual, 3 rare, -1 antichamber


rooms = {
    #yellow rooms
    'Bookshop':{
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,1]},

    'Casino':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,1]},


    'Commissary':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1]},

    'GiftShop':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,1,0,1]},

    'Kitchen':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,0,1]},


    'LaundryRoom':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,0]},

    'Locksmith':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,0]},

    'Showroom':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,1,0]},

    'TheArmory':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1]},

    'TradingPost':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,0]},

    #blue rooms
    'Antechamber':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': -1, 
        'doors': [1,1,1,1]},

    'Aquarium':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,1,0,1]},

    # 'Attic':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 0,
    #     'rarity': 3, 
    #     'doors': [1,0,0,0]},

    # 'Ballroom':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 2, 
    #     'key': 0,
    #     'rarity': 2, 
    #     'doors': [1,0,1,0]},
        
    'BilliardRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,0,1]},
        
    # 'BoilerRoom':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 0,
    #     'rarity': 2, 
    #     'doors': [1,0,1,1]},
        
    # 'ChamberofMirrors':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 0,
    #     'rarity': 3, 
    #     'doors': [1,0,0,0]},
        
    # 'Classroom':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 0,
    #     'rarity': 2, 
    #     'doors': [1,0,0,1]},
        
    # 'ClockTower':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 1,
    #     'rarity': 2, 
    #     'doors': [1,0,0,0]},
        
    # 'Closet':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 2, 
    #     'key': 1,
    #     'rarity': 0, 
    #     'doors': [1,0,0,0]},
        
    # 'CoatCheck':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 0,
    #     'rarity': 3, 
    #     'doors': [1,0,0,0]},
        
    # 'ConferenceRoom':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 0,
    #     'rarity': 2, 
    #     'doors': [1,1,1,0]},
        
    'Den':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 1, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,1,0,1]},
        
    # 'DiningRoom':'blue',
    # 'Dovecote':'blue',
    # 'DraftingStudio':'blue',
    # 'DrawingRoom':'blue',
    'EntranceHall':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': -1, 
        'doors': [0,1,1,1]},
        
    # 'Freezer':'blue',
    'Gallery':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,1,0]},
        
    'Garage':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 3,
        'rarity': 2, 
        'doors': [1,0,0,0]},
        
    # 'Laboratory':'blue',
    # 'Library':'blue',
    'LockerRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,1,0]},
        
    # 'MailRoom':'blue',
    # 'Mechanarium':'blue',
    'MusicRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 2,
        'rarity': 2, 
        'doors': [1,0,0,1]},
        
    'Nook':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 1,
        'rarity': 0, 
        'doors': [1,0,0,1]},
        
    # 'Observatory':'blue',
    'Office':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1]},
        
    'Pantry':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 4,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,0,1]},
        
    # 'Parlor':'blue',
    # 'Planetarium':'blue',
    # 'PumpRoom':'blue',
    # 'Room46':'blue',
    # 'Room8':'blue',
    # 'Rotunda':'blue',
    'RumpusRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 8,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,1,0]},
        
    # 'Schoolhouse':'blue',
    # 'Security':'blue',
    # 'Shelter':'blue',
    # 'Shrine':'blue',
    'SpareRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,1.0]},
        
    'Storeroom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 1,
        'gem': 1, 
        'key': 1,
        'rarity': 0, 
        'doors': [1,0,0,0]},
        
    # 'Study':'blue',
    # 'TheKennel':'blue',
    # 'ThePool':'blue',
    # 'ThroneRoom':'blue',
    # 'Tomb':'blue',
    # 'Toolshed':'blue',
    'TreasureTrove':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 5,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,1]},
        
    'TrophyRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 5, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,1]},
        
    # 'UtilityCloset':'blue',
    'Vault':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 40,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,0]},
        
    'WalkinCloset':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 2,
        'gem': 0, 
        'key': 2,
        'rarity': 1, 
        'doors': [1,0,0,0]},
        
    'WineCellar':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 3, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,0]},
        
    # 'Workshop':'blue',

    #orange rooms
    'Corridor':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,1,0]},


    'EastWingHall':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,1,0,1]},

    # 'Foyer':'orange',
    # 'GreatHall':'orange',
    'Hallway':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,1,0,1]},

    'Passageway':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,1,1,1]},

    # 'SecretPassage':'orange',
    # 'Tunnel':'orange',
    # 'Vestibule':'orange',
    'WestWingHall':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,1,0,1]},


    #violet rooms
    'Bedroom':{        
        'color': 'violet', 
        'step': 2, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,1]},

    'Boudoir':{        
        'color': 'violet', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1]},

    'BunkRoom':{        
        'color': 'violet', 
        'step': 5, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,0]},

    # 'Dormitory':'violet',
    'GuestBedroom':{        
        'color': 'violet', 
        'step': 10, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,0,0]},

    # 'HerLadyshipsChamber':'violet',
    # 'Hovel':'violet',
    # 'MasterBedroom':'violet',
    # 'Nursery':'violet',
    # 'ServantsQuarters':'violet',

    #green rooms
    'Cloister':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,1,1,1]},

    # 'Conservatory':'green',
    'Courtyard':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,1,0,1]},

    # 'Greenhouse':'green',
    'MorningRoom':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 2, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,1,0,0]},

    'Patio':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1]},

    # 'RootCellar':'green',
    'SecretGarden':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,1,0,1]},

    # 'Solarium':'green',
    # 'Terrace':'green',
    # 'Veranda':'green',

    #red rooms
    # 'Archives':'red',
    'Chapel':{        
        'color': 'red', 
        'step': 0, 
        'coin': -1,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,1,0,1]},

    # 'ClosedExhibit':'red',
    # 'Darkroom':'red',
    # 'Furnace':'red',
    # 'Gymnasium':'red',
    'Lavatory':{        
        'color': 'red', 
        'step': 0, 
        'coin': -1,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,1,0,1]},
        
    # 'Lost&Found':'red',
    # 'MaidsChamber':'red',
    # 'WeightRoom':'red'
}

