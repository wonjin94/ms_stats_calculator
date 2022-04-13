# Some values include ones with wrong spelling, top one has the correct spelling
equip_type_dict = {
    # [has flame, column name on google sheet]
    "RING" : [False,["B","C","D","E"]],
    "RNG" : [False,["B","C","D","E"]],

    "POCKET ITEM": [True,"F"],

    "PENDANT" : [True,["G","H"]],
    "PENOANT" : [True,["G","H"]],

    "POLE ARM": [True,"I"],
    "BELT" : [True,"J"],
    "HAT" : [True,"K"],
    "FACE ACCESSORY": [True,"L"],
    "EYE ACCESSORY" : [True,"M"],
    "TOP" : [True,"N"],
    "BOTTOM" : [True,"O"],
    "SHOES" : [True,"P"],

    "EARRINGS" : [True,"Q"],
    "EARRNGS" : [True,"Q"],


    "SHOULDER" : [False, "R"],
    "GLOVES" : [True,"S"],
    "EMBLEM" : [False,"T"],
    "BADGE" : [False,"U"],
    "MEDAL" : [False,"V"],
    "Mass" :[False,"W"],
    "CAPE" : [True,"X"],
    "MECHANICAL HEART" : [False, "Y"]
}

stat_dict = {
    # row number on google sheet
    # [ total, Flame ]
    "STR" : [5,12],
    "SR" : [5,12],

    "DEX" : [6,13],
    "Attack Power" : [9,16],
    "Altack Power" : [9,16],

    # no flame
    "Ignored Enemy DEF" : [11],

    # only flames
    "All Stats" : [18],
    "Al Stats" : [18],

    
    "Boss Damage" : [20]
}

potential_dict = {
    "STR" : 21,
    "SR" : 21,
    
    "DEX" : 25,
    
    "All Stats" : 22,
    "Al Stats" : 22,
    
    "ATT" : 23,
    "Boss Monster Damage" : 24,

    "Critical Damage" : 26,
    "Criical Damage" : 26
    
    
}