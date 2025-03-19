companion_data = {
    "companion":{
    "id": "companion",
    "health": 100,
    "attack": 50,
    "defense": 30,
    "name": "Companion A",
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "companion",
        "has_traits": {}
    }
}

# Example creature_data dictionary (with default traits)
creature_data = {
    "dragon": {
        "id": "dragon",
        "name": "Flame Wyvern",
        "health": 100,
        "attack": 50,
        "defense": 30,
        "hates_all": True,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "dragon",
        "has_traits": {
            "scales": "Impenetrable",
            "hoard_guarding": "Aggressive"
        }},
    "goblin": {
        "id": "goblin",
        "name": "Small sneaky goblin",
        "health": 50,
        "attack": 12,
        "defense": 5,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": ["animal"],
        "monster_type": "goblin",
        "has_traits": {}
    },
    "wolf": {
        "id": "wolf",
        "name": "Young wolf",
        "health": 60,
        "attack": 15,
        "defense": 7,
        "hates_all": True,
        "hates_player_and_companions": False,
        "monster_type": "wolf",
        "has_traits": {}
    },
    "rabbit": {
        "id": "rabbit",
        "name": "Small rabbit",
        "health": 30,
        "attack": 5,
        "defense": 2,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "rabbit",
        "has_traits": {}
        }
    }


# Example creature_traits dictionary (optional traits)
creature_traits_data = {
    "flight": True,
    "regeneration": "Moderate",
    "fire_resistance": "High",
    "poison_immunity": True
}

# Example creature_status_data dictionary (default status effects)
creature_status_data = {
    "status_effect": {
        "buffs": {
            "strength_boost": [0, 0]  # Default duration and effect
        },
        "debuffs": {
            "poisoned": [0, 0]  # Default duration and effect
        }
    }
}

player_data = {
    "player":{
        "id": "player",
        "health": 200,
        "attack": 50,
        "defense": 30,
        "name": "Claus",
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "player",
        "has_traits": {
            "admin": "Mysterious admin powers"
        }
    }
}
