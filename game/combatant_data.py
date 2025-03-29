# In game/combatant_data.py

companion_data = {
    "companion": {
        "id": "companion",
        "health": 100,
        "attack": 50,
        "defense": 30,
        "strength": 5,  # Added strength
        "intelligence": 2,  # Added intelligence
        "level": 1,
        "name": "Companion A",
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "companion",
        "has_traits": {}
    }
}

creature_data = {
    "goblin": {
        "id": "goblin",
        "name": "Small sneaky goblin",
        "health": 5,
        "attack": 2,
        "defense": 2,
        "strength": 3,  # Added strength
        "intelligence": 1,  # Added intelligence
        "level": 1,
        "health_per_level": 5,
        "attack_per_level": 3,
        "defense_per_level": 2,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": ["animal"],
        "monster_type": "goblin",
        "has_traits": {}
    },
    "dragon": {
        "id": "dragon",
        "name": "Flame Wyvern",
        "health": 2000,
        "attack": 4,
        "defense": 4,
        "strength": 2,  # Added strength
        "intelligence": 5,  # Added intelligence
        "level": 1,
        "health_per_level": 20,
        "attack_per_level": 5,
        "defense_per_level": 4,
        "hates_all": True,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "dragon",
        "has_traits": {"fire_breath": True}
    },
    "wolf": {
        "id": "wolf",
        "name": "Young wolf",
        "health": 10,
        "attack": 3,
        "defense": 4,
        "strength": 4,  # Added strength
        "intelligence": 1,  # Added intelligence
        "level": 1,
        "health_per_level": 10,
        "attack_per_level": 5,
        "defense_per_level": 4,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": ["animal"],
        "monster_type": "wolf",
        "has_traits": {}
    },
    "rabbit": {
        "id": "rabbit",
        "name": "Small rabbit",
        "health": 3,
        "attack": 1,
        "defense": 1,
        "strength": 1,  # Added strength
        "intelligence": 1,  # Added intelligence
        "level": 1,
        "health_per_level": 4,
        "attack_per_level": 1,
        "defense_per_level": 1,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "rabbit",
        "has_traits": {}
    }
}

player_data = {
    "player": {
        "id": "player",
        "health": 200,
        "attack": 50,
        "defense": 30,
        "strength": 5,  # Added strength
        "intelligence": 3,  # Added intelligence
        "level": 1,
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
