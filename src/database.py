#names used for images loading in Display

consumables = ['steps', 'coin', 'gem', 'key', 'dice'] #sets the order on screen
permanents = ['Shovel','Lockpick_Kit','Lucky_Rabbits_Foot','Metal_Detector','Power_Hammer']

#|-2-|
#3   1          doors = [0,1,2,3]
#|_0_|

#rarity : 0 common, 1 standard, 2 unusual, 3 rare, -1 antechamber

"""effects : 0- no effects
             1- spread gem in rooms
             2- spread keys in rooms
             3- spread coins in rooms
             4- spread fruits in rooms

             5- modify the rarity of a room                done
             6- modify the probability of objects          

             7- add a new room (unlock)                 

             8- set the gen number                         done
             9- divide by 2 step num                       done


"""

rooms = {
    #yellow rooms
    'Bookshop':{
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,1],
        'effect': 0},

    'Casino':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,1],
        'effect': 0},


    'Commissary':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1],
        'effect': 0},

    'GiftShop':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,1,0,1],
        'effect': 0},

    'Kitchen':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,0,1],
        'effect': 0},


    'LaundryRoom':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,0],
        'effect': 0},

    'Locksmith':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,0],
        'effect': 0},

    'Showroom':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,1,0],
        'effect': 0},

    'TheArmory':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1],
        'effect': 0},

    'TradingPost':{        
        'color': 'yellow', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,0],
        'effect': 0},

    #blue rooms
    'Antechamber':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': -1, 
        'doors': [1,1,1,1],
        'effect': 0},

    'Aquarium':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,1,0,1],
        'effect': 0},

    # 'Attic':{        
    #     'color': 'blue', 
    #     'step': 0, 
    #     'coin': 0,
    #     'gem': 0, 
    #     'key': 0,
    #     'rarity': 3, 
    #     'doors': [1,0,0,0]},

    'Ballroom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 2, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,1,0],
        'effect': 8},
        
    'BilliardRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,0,1],
        'effect': 0},
        
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
        'doors': [1,1,0,1],
        'effect': 0},
        
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
        'doors': [0,1,1,1],
        'effect': 0},
        
    # 'Freezer':'blue',
    'Gallery':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,1,0],
        'effect': 0},
        
    'Garage':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 3,
        'rarity': 2, 
        'doors': [1,0,0,0],
        'effect': 0},
        
    # 'Laboratory':'blue',
    # 'Library':'blue',
    'LockerRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,1,0],
        'effect': 2},
        
    # 'MailRoom':'blue',
    # 'Mechanarium':'blue',
    'MusicRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 2,
        'rarity': 2, 
        'doors': [1,0,0,1],
        'effect': 0},
        
    'Nook':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 1,
        'rarity': 0, 
        'doors': [1,0,0,1],
        'effect': 0},
        
    # 'Observatory':'blue',
    'Office':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1],
        'effect': 3},
        
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
        'doors': [1,0,1,0],
        'effect': 0},
        
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
        'doors': [1,0,1,0],
        'effect': 0},
        
    'Storeroom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 1,
        'gem': 1, 
        'key': 1,
        'rarity': 0, 
        'doors': [1,0,0,0],
        'effect': 0},
        
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
        'doors': [1,0,0,1],
        'effect': 0},
        
    'TrophyRoom':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 5, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,1],
        'effect': 0},
        
    # 'UtilityCloset':'blue',
    'Vault':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 40,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,0],
        'effect': 0},
        
    'WalkinCloset':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 2,
        'gem': 0, 
        'key': 2,
        'rarity': 1, 
        'doors': [1,0,0,0],
        'effect': 0},
        
    'WineCellar':{        
        'color': 'blue', 
        'step': 0, 
        'coin': 0,
        'gem': 3, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,0],
        'effect': 0},
        
    # 'Workshop':'blue',

    #orange rooms
    'Corridor':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,0,1,0],
        'effect': 0},


    'EastWingHall':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,1,0,1],
        'effect': 0},

    # 'Foyer':'orange',
    # 'GreatHall':'orange',
    'Hallway':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,1,0,1],
        'effect': 0},

    'Passageway':{        
        'color': 'orange', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,1,1,1],
        'effect': 0},

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
        'doors': [1,1,0,1],
        'effect': 0},


    #violet rooms
    'Bedroom':{        
        'color': 'violet', 
        'step': 2, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,1],
        'effect': 0},

    'Boudoir':{        
        'color': 'violet', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1],
        'effect': 0},

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
        'doors': [1,0,0,0],
        'effect': 0},

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
        'doors': [1,1,1,1],
        'effect': 0},

    # 'Conservatory':'green',
    'Courtyard':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,1,0,1],
        'effect': 0},

    'Greenhouse':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,1,0,0],
        'effect': 5},

    'MorningRoom':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 2, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,1,0,0],
        'effect': 0},

    'Patio':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,1],
        'effect': 1},

    # 'RootCellar':'green',
    'SecretGarden':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,1,0,1],
        'effect': 4},

    'Solarium':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,0],
        'effect': 5},

    # 'Terrace':'green',
    'Veranda':{        
        'color': 'green', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,1,0],
        'effect': 6},   

    #red rooms
    # 'Archives':'red',
    'Chapel':{        
        'color': 'red', 
        'step': 0, 
        'coin': -1,
        'gem': 0, 
        'key': 0,
        'rarity': 0, 
        'doors': [1,1,0,1],
        'effect': 0},  

    # 'ClosedExhibit':'red',
    # 'Darkroom':'red',
    'Furnace':{        
        'color': 'red', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,0,0,0],
        'effect': 5}, 

    'Gymnasium':{        
        'color': 'red', 
        'step': -2, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,1,0,1],
        'effect': 0}, 


    'Lavatory':{        
        'color': 'red', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 1, 
        'doors': [1,0,0,0],
        'effect': 0}, 
        
    # 'Lost&Found':'red',
    'MaidsChamber':{        
        'color': 'red', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 2, 
        'doors': [1,0,0,1],
        'effect': 6}, 

    'WeightRoom':{        
        'color': 'red', 
        'step': 0, 
        'coin': 0,
        'gem': 0, 
        'key': 0,
        'rarity': 3, 
        'doors': [1,1,1,1],
        'effect': 9}, 
}

